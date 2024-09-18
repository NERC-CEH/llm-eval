# GPU Information
This document contains information about potential data centre grade GPUs and which Large Language Models (LLMs) they could potentially support. The table purely considers the theoretical vRAM requirements of various models and which GPUs should be able to run the model for inference.
> Note: The information here does not suggest anything regarding throuput or general performance of each model on each GPU.

## Models / GPU

| Model         | Params (billions) | Bit Quantizaton | vRAM (GB) | GPU |         |      |          |          |              |
|---------------|-------------------|------|---------|-----|---------|------|----------|----------|--------------|
|               |                   |      |         | A40 | 2 x A40 | A100 | 2 x A100 | H100 NVL | 2 x H100 NVL |
|               |                   |      |         | 48GB  | 96GB      | 80GB   | 160GB      | 94GB       | 188GB          |
| [`llama3.1:8B`](https://ollama.com/library/llama3.1)      | 8                 | 4    | 4.47    | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 8                 | 8    | 8.94    | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 8                 | 16   | 17.88   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
| [`llama3.1 :70B`](https://ollama.com/library/llama3.1:70b)    | 70                | 4    | 39.12   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 70                | 8    | 78.23   |     | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 70                | 16   | 156.46  |     |         |      | ✓        |          | ✓            |
| [`gemma2:9B`](https://ollama.com/library/gemma2)        | 9                 | 4    | 5.03    | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 9                 | 8    | 10.06   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 9                 | 16   | 20.12   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
| [`gemma2:27B`](https://ollama.com/library/gemma2:27b)      | 27                | 4    | 15.09   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 27                | 8    | 30.17   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 27                | 16   | 60.35   |     | ✓       | ✓    | ✓        | ✓        | ✓            |
| [`mistral`](https://ollama.com/library/mistral)       | 7                 | 4    | 3.91    | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 7                 | 8    | 7.82    | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 7                 | 16   | 15.65   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
| [`mistral-nemo`](https://ollama.com/library/mistral-nemo)  | 12                | 4    | 6.71    | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 12                | 8    | 13.41   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 12                | 16   | 26.82   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
| [`mistral-small`](https://ollama.com/library/mistral-small) | 22                | 4    | 12.29   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 22                | 8    | 24.59   | ✓   | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 22                | 16   | 49.17   |     | ✓       | ✓    | ✓        | ✓        | ✓            |
| [`mistral-large`](https://ollama.com/library/mistral-large) | 123               | 4    | 68.73   |     | ✓       | ✓    | ✓        | ✓        | ✓            |
|               | 123               | 8    | 137.46  |     |         |      | ✓        |          | ✓            |
|               | 123               | 16   | 274.93  |     |         |      |          |          |              |

> Note: The vRam requirement is an estiomate calculated based on the number of paramaters, the quantization used, and including a 20% overhead i.e. vRAM = ((No. params x quantization bits)/8) x 1.2