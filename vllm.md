# Out of memory issues
[vLLM](https://docs.vllm.ai/en/latest/) can download models directly from HuggingFace repositories. Unfortunately the library will attempt to pre-allocate vRAM space on the GPU for the model it is downloading, meaning if the model is too large for the vRAM that is available you will receive an out of memory error (without the model even having been downloaded).

The easiest way to avoid this issue is to download models that have been pre-quantized and will therefore more likely be small enough to fit in available vRAM. [UnslothAI](https://docs.unsloth.ai/get-started/all-our-models) has a lot of the popular models available in pre-quantized forms. These can be downloaded and used very easily, but you have to specify the quantization and load methods when doing so ([`bitsandbytes`](https://github.com/bitsandbytes-foundation/bitsandbytes)):

```python
llm = LLM(model="unsloth/Mistral-Nemo-Instruct-2407-bnb-4bit", quantization="bitsandbytes", load_format="bitsandbytes", max_model_len=4096)
```
> Note: vLLM will also ensure that enough memory is available to hold the context for queries run on the model. If the model has a very large context window this can easily create another out of memory exception. Set `max_model_len` to a reasonably small number to ensure no further memory issues.