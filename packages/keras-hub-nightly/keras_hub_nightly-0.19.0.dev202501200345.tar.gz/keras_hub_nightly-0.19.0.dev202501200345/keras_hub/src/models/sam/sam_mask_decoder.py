import keras
from keras import ops

from keras_hub.src.api_export import keras_hub_export
from keras_hub.src.models.sam.sam_layers import MLP
from keras_hub.src.models.sam.sam_transformer import TwoWayTransformer


@keras_hub_export("keras_hub.layers.SAMMaskDecoder")
class SAMMaskDecoder(keras.layers.Layer):
    """Mask decoder for the Segment Anything Model (SAM).

    This lightweight module efficiently maps the image embedding and a set of
    prompt embeddings to an output mask. Before applying the transformer
    decoder, the layer first inserts into the set of prompt embeddings a
    learned output token embedding that will be used at the decoder's output.
    For simplicity, these embeddings (not including the image embedding) are
    collectively called "tokens".

    The image embeddings, positional image embeddings, and tokens are passed
    through a transformer decoder. After running the decoder, the layer
    upsamples the updated image embedding by 4x with two transposed
    convolutional layers (now it's downscaled 4x relative to the input
    image). Then, the tokens attend once more to the image embedding and
    the updated output token embedding are passed to a small 3-layer MLP that
    outputs a vector matching the channel dimension of the upscaled image
    embedding.

    Finally, a mask is predicted with a spatially point-wise
    product between the upscaled image embedding and the MLP's output.

    Args:
        hidden_size: int. The hidden size of the TwoWayTransformer.
        num_layers: int. The number of layers in the TwoWayTransformer.
        intermediate_dim: int. The intermediate dimension of the
            TwoWayTransformer.
        num_heads: int. The number of heads in the TwoWayTransformer.
        embedding_dim: int, optional. The number of input features to the
            transformer decoder. Defaults to `256`.
        num_multimask_outputs: int, optional. Number of multimask outputs.
            The model would generate these many extra masks. The total masks
            generated by the model are `1 + num_multimask_outputs`. Defaults
            to `3`.
        iou_head_depth: int, optional. The depth of the dense net used to
            predict the IoU confidence score. Defaults to `3`.
        iou_head_hidden_dim: int, optional. The number of units in the hidden
            layers used in the dense net to predict the IoU confidence score.
            Defaults to `256`.
        activation: str, optional. Activation to use in the mask upscaler
            network. Defaults to `"gelu"`.
    """

    def __init__(
        self,
        *,
        hidden_size,
        num_layers,
        intermediate_dim,
        num_heads,
        embedding_dim=256,
        num_multimask_outputs=3,
        iou_head_depth=3,
        iou_head_hidden_dim=256,
        activation="gelu",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.intermediate_dim = intermediate_dim
        self.num_heads = num_heads
        self.embedding_dim = embedding_dim
        transformer = TwoWayTransformer(
            num_layers=num_layers,
            hidden_size=hidden_size,
            intermediate_dim=intermediate_dim,
            num_heads=num_heads,
            dtype=self.dtype_policy,
        )
        self.transformer = transformer
        self.num_multimask_outputs = num_multimask_outputs
        self.iou_head_depth = iou_head_depth
        self.iou_head_hidden_dim = iou_head_hidden_dim
        self.activation = activation

        self.iou_token = keras.layers.Embedding(
            1, embedding_dim, dtype=self.dtype_policy
        )
        self.num_mask_tokens = num_multimask_outputs + 1
        self.mask_tokens = keras.layers.Embedding(
            self.num_mask_tokens, embedding_dim, dtype=self.dtype_policy
        )

        self.output_upscaling = keras.models.Sequential(
            [
                keras.layers.Conv2DTranspose(
                    embedding_dim // 4,
                    kernel_size=2,
                    strides=2,
                    dtype=self.dtype_policy,
                ),
                keras.layers.LayerNormalization(
                    epsilon=1e-6, dtype=self.dtype_policy
                ),
                keras.layers.Activation(activation, dtype=self.dtype_policy),
                keras.layers.Conv2DTranspose(
                    embedding_dim // 8,
                    kernel_size=2,
                    strides=2,
                    dtype=self.dtype_policy,
                ),
                keras.layers.Activation(activation, dtype=self.dtype_policy),
            ]
        )

        self.output_hypernetworks_mlps = [
            MLP(embedding_dim, embedding_dim // 8, 3, dtype=self.dtype_policy)
            for _ in range(self.num_mask_tokens)
        ]

        self.iou_prediction_head = MLP(
            iou_head_hidden_dim,
            self.num_mask_tokens,
            iou_head_depth,
            dtype=self.dtype_policy,
        )

    def build(self, input_shape=None, **kwargs):
        self.transformer.build()
        self.iou_token.build([None])
        self.mask_tokens.build([None])
        self.output_upscaling.build([None, None, None, self.embedding_dim])
        for mlp in self.output_hypernetworks_mlps:
            mlp.build([None, self.embedding_dim])
        self.iou_prediction_head.build([None, self.embedding_dim])
        self.built = True

    def call(
        self,
        image_embeddings,
        prompt_dense_positional_embeddings,
        prompt_sparse_embeddings,
        prompt_dense_embeddings,
    ):
        masks, iou_pred = self._predict_masks(
            image_embeddings=image_embeddings,
            image_positional_embeddings=prompt_dense_positional_embeddings,
            prompt_sparse_embeddings=prompt_sparse_embeddings,
            prompt_dense_embeddings=prompt_dense_embeddings,
        )

        return {"masks": masks, "iou_pred": iou_pred}

    def _predict_masks(
        self,
        image_embeddings,
        image_positional_embeddings,
        prompt_sparse_embeddings,
        prompt_dense_embeddings,
    ):
        indices_iou = ops.arange(1, dtype="int32")
        indices_mask = ops.arange(self.num_mask_tokens, dtype="int32")

        output_tokens = ops.concatenate(
            [self.iou_token(indices_iou), self.mask_tokens(indices_mask)],
            axis=0,
        )
        output_tokens = ops.broadcast_to(
            output_tokens[None, ...],
            shape=(
                ops.shape(prompt_sparse_embeddings)[0],
                ops.shape(output_tokens)[0],
                ops.shape(output_tokens)[1],
            ),
        )
        tokens = ops.concatenate(
            [output_tokens, prompt_sparse_embeddings], axis=1
        )

        source = ops.broadcast_to(
            image_embeddings,
            shape=(
                ops.shape(tokens)[0],
                ops.shape(image_embeddings)[1],
                ops.shape(image_embeddings)[2],
                ops.shape(image_embeddings)[3],
            ),
        )
        source = source + prompt_dense_embeddings
        positional_source = ops.broadcast_to(
            image_positional_embeddings,
            shape=(
                ops.shape(tokens)[0],
                ops.shape(image_embeddings)[1],
                ops.shape(image_embeddings)[2],
                ops.shape(image_embeddings)[3],
            ),
        )
        shape = ops.shape(source)
        batch_dim, height, width, channels = (
            shape[0],
            shape[1],
            shape[2],
            shape[3],
        )

        hidden_state, source = self.transformer(
            source, positional_source, tokens
        )
        iou_token_out = hidden_state[:, 0, :]
        mask_tokens_out = hidden_state[:, 1 : (1 + self.num_mask_tokens), :]

        source = ops.reshape(source, (batch_dim, height, width, channels))
        upscaled_embeddings = self.output_upscaling(source)
        hyper_in_list = []
        for i in range(self.num_mask_tokens):
            hyper_in_list.append(
                self.output_hypernetworks_mlps[i](mask_tokens_out[:, i, :])
            )
        hyper_in = ops.stack(hyper_in_list, axis=1)
        shape = ops.shape(upscaled_embeddings)
        batch_dim, height, width, channels = (
            shape[0],
            shape[1],
            shape[2],
            shape[3],
        )
        upscaled_embeddings = ops.reshape(
            ops.transpose(upscaled_embeddings, axes=(0, 3, 1, 2)),
            (batch_dim, channels, height * width),
        )
        masks = ops.reshape(
            hyper_in @ upscaled_embeddings,
            (batch_dim, self.num_mask_tokens, height, width),
        )

        iou_pred = self.iou_prediction_head(iou_token_out)

        return masks, iou_pred

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "hidden_size": self.hidden_size,
                "num_layers": self.num_layers,
                "intermediate_dim": self.intermediate_dim,
                "num_heads": self.num_heads,
                "embedding_dim": self.embedding_dim,
                "num_multimask_outputs": self.num_multimask_outputs,
                "iou_head_depth": self.iou_head_depth,
                "iou_head_hidden_dim": self.iou_head_hidden_dim,
                "activation": self.activation,
            }
        )
        return config
