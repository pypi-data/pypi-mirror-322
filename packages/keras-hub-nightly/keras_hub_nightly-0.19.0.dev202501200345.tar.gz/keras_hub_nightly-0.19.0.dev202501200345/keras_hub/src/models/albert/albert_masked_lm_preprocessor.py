from keras_hub.src.api_export import keras_hub_export
from keras_hub.src.models.albert.albert_backbone import AlbertBackbone
from keras_hub.src.models.albert.albert_tokenizer import AlbertTokenizer
from keras_hub.src.models.masked_lm_preprocessor import MaskedLMPreprocessor


@keras_hub_export("keras_hub.models.AlbertMaskedLMPreprocessor")
class AlbertMaskedLMPreprocessor(MaskedLMPreprocessor):
    """ALBERT preprocessing for the masked language modeling task.

    This preprocessing layer will prepare inputs for a masked language modeling
    task. It is primarily intended for use with the
    `keras_hub.models.AlbertMaskedLM` task model. Preprocessing will occur in
    multiple steps.

    - Tokenize any number of input segments using the `tokenizer`.
    - Pack the inputs together with the appropriate `"<s>"`, `"</s>"` and
      `"<pad>"` tokens, i.e., adding a single `"<s>"` at the start of the
      entire sequence, `"</s></s>"` between each segment,
      and a `"</s>"` at the end of the entire sequence.
    - Randomly select non-special tokens to mask, controlled by
      `mask_selection_rate`.
    - Construct a `(x, y, sample_weight)` tuple suitable for training with a
      `keras_hub.models.AlbertMaskedLM` task model.

    Args:
        tokenizer: A `keras_hub.models.AlbertTokenizer` instance.
        sequence_length: The length of the packed inputs.
        mask_selection_rate: The probability an input token will be dynamically
            masked.
        mask_selection_length: The maximum number of masked tokens supported
            by the layer.
        mask_token_rate: float. `mask_token_rate` must be
            between 0 and 1 which indicates how often the mask_token is
            substituted for tokens selected for masking.
            Defaults to `0.8`.
        random_token_rate: float. `random_token_rate` must be
            between 0 and 1 which indicates how often a random token is
            substituted for tokens selected for masking. Default is 0.1.
            Note: mask_token_rate + random_token_rate <= 1,  and for
            (1 - mask_token_rate - random_token_rate), the token will not be
            changed. Defaults to `0.1`.
        truncate: string. The algorithm to truncate a list of batched segments
            to fit within `sequence_length`. The value can be either
            `round_robin` or `waterfall`:
            - `"round_robin"`: Available space is assigned one token at a
                time in a round-robin fashion to the inputs that still need
                some, until the limit is reached.
            - `"waterfall"`: The allocation of the budget is done using a
                "waterfall" algorithm that allocates quota in a
                left-to-right manner and fills up the buckets until we run
                out of budget. It supports an arbitrary number of segments.

    Examples:

    Directly calling the layer on data.
    ```python
    preprocessor = keras_hub.models.AlbertMaskedLMPreprocessor.from_preset(
        "albert_base_en_uncased"
    )

    # Tokenize and mask a single sentence.
    preprocessor("The quick brown fox jumped.")

    # Tokenize and mask a batch of single sentences.
    preprocessor(["The quick brown fox jumped.", "Call me Ishmael."])

    # Tokenize and mask sentence pairs.
    # In this case, always convert input to tensors before calling the layer.
    first = tf.constant(["The quick brown fox jumped.", "Call me Ishmael."])
    second = tf.constant(["The fox tripped.", "Oh look, a whale."])
    preprocessor((first, second))
    ```

    Mapping with `tf.data.Dataset`.
    ```python
    preprocessor = keras_hub.models.AlbertMaskedLMPreprocessor.from_preset(
        "albert_base_en_uncased"
    )

    first = tf.constant(["The quick brown fox jumped.", "Call me Ishmael."])
    second = tf.constant(["The fox tripped.", "Oh look, a whale."])

    # Map single sentences.
    ds = tf.data.Dataset.from_tensor_slices(first)
    ds = ds.map(preprocessor, num_parallel_calls=tf.data.AUTOTUNE)

    # Map sentence pairs.
    ds = tf.data.Dataset.from_tensor_slices((first, second))
    # Watch out for tf.data's default unpacking of tuples here!
    # Best to invoke the `preprocessor` directly in this case.
    ds = ds.map(
        lambda first, second: preprocessor(x=(first, second)),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    ```
    """

    backbone_cls = AlbertBackbone
    tokenizer_cls = AlbertTokenizer
