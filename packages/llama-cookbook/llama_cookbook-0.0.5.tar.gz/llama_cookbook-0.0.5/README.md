# Llama Cookbook: The Official Guide to building with Llama Models

Welcome to the official repository for helping you get started with [inference](./getting-started/inference/), [fine-tuning](./getting-started/finetuning) and [end-to-end use-cases](./end-to-end-use-cases) of building with the Llama Model family.

This repository covers the most popular community approaches, use-cases and the latest recipes for Llama Text and Vision models.

> [!TIP]
> Popular getting started links:
> * [Build with Llama Tutorial](./getting-started/build_with_Llama_3_2.ipynb)
> * [Multimodal Inference with Llama 3.2 Vision](./getting-started/inference/local_inference/README.md#multimodal-inference)
> * [Inferencing using Llama Guard (Safety Model)](./end-to-end-use-cases/responsible_ai/llama_guard/)

> [!TIP]
> Popular end to end recipes:
> * [Email Agent](./end-to-end-use-cases/email_agent/)
> * [NotebookLlama](./end-to-end-use-cases/NotebookLlama/)
> * [Text to SQL](./end-to-end-use-cases/coding/text2sql/)


> Note: We recently did a refactor of the repo, [archive-main](https://github.com/meta-llama/llama-cookbook/tree/archive-main) is a snapshot branch from before the refactor

## Repository Structure:

- [3P Integrations](./3p-integrations): Getting Started Recipes and End to End Use-Cases from various Llama providers
- [End to End Use Cases](./end-to-end-use-cases): As the name suggests, spanning various domains and applications
- [Getting Started](./getting-started/): Reference for inferencing, fine-tuning and RAG examples
- [src](./src/): Contains the src for the original llama-recipes library along with some FAQs for fine-tuning.

## FAQ: 

- Q: What happened to llama-recipes?

A: We recently renamed llama-recipes to llama-cookbook

- Q: Prompt Template changes for Multi-Modality? 

A: Llama 3.2 follows the same prompt template as Llama 3.1, with a new special token `<|image|>` representing the input image for the multimodal models.

More details on the prompt templates for image reasoning, tool-calling and code interpreter can be found [on the documentation website](https://llama.meta.com/docs/model-cards-and-prompt-formats/llama3_2).

- Q: I have some questions for Fine-Tuning, is there a section to address these?

A: Checkout the Fine-Tuning FAQ [here](./src/docs/)

- Q: Some links are broken/folders are missing: 

A: We recently did a refactor of the repo, [archive-main](https://github.com/meta-llama/llama-cookbook/tree/archive-main) is a snapshot branch from before the refactor

- Where can we find details about the latest models?

A: Official [Llama models website](https://www.llama.com)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License
<!-- markdown-link-check-disable -->

See the License file for Meta Llama 3.2 [here](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/LICENSE) and Acceptable Use Policy [here](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/USE_POLICY.md)

See the License file for Meta Llama 3.1 [here](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/LICENSE) and Acceptable Use Policy [here](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/USE_POLICY.md)

See the License file for Meta Llama 3 [here](https://github.com/meta-llama/llama-models/blob/main/models/llama3/LICENSE) and Acceptable Use Policy [here](https://github.com/meta-llama/llama-models/blob/main/models/llama3/USE_POLICY.md)

See the License file for Meta Llama 2 [here](https://github.com/meta-llama/llama-models/blob/main/models/llama2/LICENSE) and Acceptable Use Policy [here](https://github.com/meta-llama/llama-models/blob/main/models/llama2/USE_POLICY.md)
<!-- markdown-link-check-enable -->
