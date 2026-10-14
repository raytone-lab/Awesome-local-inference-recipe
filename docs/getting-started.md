# Getting started

[English](getting-started.md) | [简体中文](getting-started.zh-CN.md)

How to pick a recipe for your budget and hardware, then run it.

## 1. Pick by what you already have
| You have | Start with | Typical engines |
|---|---|---|
| Mac (Apple Silicon, ≥32 GB unified memory) | Mac recipes; the larger the memory, the larger the model | MLX, oMLX, llama.cpp, mlx-serve |
| NVIDIA consumer GPU (RTX 3090/4090/5090…) | Models whose quantized size fits in VRAM, or MoE models with offload | llama.cpp, vLLM, SGLang, ExLlama, Strata |
| DGX Spark | 128 GB unified memory; large MoE models | vLLM, TensorFold, ExLlama |
| AMD (Strix Halo, Radeon) | Strix Halo for large models in unified memory | llama.cpp (HIP/Vulkan), Strata, Halogen |
| Used datacenter cards (V100, etc.) | Cheap VRAM per dollar; check driver/CUDA support | llama.cpp, Strata |

Buying hardware? Use the budget tiers in the [README](../README.md) (up to $2.5k / $7k / $14k / $30k).

## 2. Read a recipe
Each row is model × engine × hardware → number. Check the **source level** first: ✅ measured and 🏛️ official are stronger than 🔁 relayed and 📣 claimed. Filter in the [explorer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html) by hardware, model family, engine and tags (e.g. `4bit`, `MoE`).

## 3. Run it
1. Open the [guide page](../recipes/README.md) if the recipe has one, otherwise the source link.
2. Download the exact model file and quantization listed (usually from Hugging Face).
3. Install the engine version named in the recipe; forks are called out explicitly.
4. Use the launch command from the source. If it is marked "not published", follow the source post — do not guess flags.
5. Compare your speed with the same context length and prompt length as the source.

## 4. Share your result
Open a recipe submission issue or PR — see [CONTRIBUTING](../CONTRIBUTING.md).
