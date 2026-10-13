# Awesome Local Inference Recipes [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Model × engine × hardware → measured speed and cost, with every number linked to its source. Consumer and used hardware, ≤ $30k.
> 本地推理配方：跨引擎、消费级/二手硬件、每个数字标来源。

<sub>Working name: **RecipeBench** (placeholder) · {{N}} recipes ({{NT}} text · {{NI}} image · {{NV}} video/audio) · data as of 2026-10-13 · <a href="explore.html">Explorer</a> · <a href="submit.html">Submit</a></sub>

## Contents

{{TOC}}

## Legend

| Source level | | Format |
|---|---|---|
| 🏛️ **官方** Official | vendor/project number | `Model · Engine` `quant` — Hardware → **key number** level [source] |
| ✅ **实测** Measured | author ran it, log/screenshot | **tok/s** = single-stream generation (not prefill, not aggregate) |
| 🔁 **转述** Relayed | second-hand, verify upstream | Tiers use the lowest published hardware price (USD) |
| 📣 **宣称** Claimed | projection, no repro | Unknown fields are never estimated (未见公开数据) |
<!--RECIPES-->

## Engines & Tools

- [Strata](https://github.com/Niko1221/Strata) - MoE engine that splits experts across GPU, RAM and SSD for 12–24GB cards. Most Flash-Next recipes here use it.
- [oMLX](https://github.com/jundot/omlx) - Apple Silicon MLX server with continuous batching and tiered KV/SSD cache.
- [DFlash / DFlash 2](https://github.com/z-lab/dflash) - Block-diffusion speculative decoding with drafts for Qwen3.8-27B. MLX port: [dflash-mlx](https://github.com/bstnxbt/dflash-mlx).
- [TensorFold](https://github.com/ashhart/TensorFold) - OpenAI-compatible MoE runtime with speculative decoding. Also used for MiniMax H3 in ComfyUI.
- [FastH3](https://haoailab.com/blogs/fasth3-rtx/) - Hao AI Lab's 8-step distilled MiniMax H3 for RTX cards.
- [LightX2V](https://github.com/ModelTC/LightX2V) - Video generation inference framework, with MiniMax H3 results on a 5090.
- [halogen](https://github.com/peonist-ai/halogen-flash-server/) - Flash-Next server tuned for Strix Halo.
- [llama.cpp](https://github.com/ggml-org/llama.cpp) - The baseline GGUF engine for CPU, CUDA, ROCm, Vulkan and Metal.
- [MLX](https://github.com/ml-explore/mlx) - Apple's array framework behind most Mac recipes.
- [vLLM](https://github.com/vllm-project/vllm) - High-throughput server. MTP and multi-stream recipes on Spark.
- [SGLang](https://github.com/sgl-project/sglang) - Serving framework, paired with DFlash2 on DGX Spark.

## Related Lists & Benchmarks

- [llamabench.ai](https://llamabench.ai/) - llama.cpp results with full launch commands.
- [llamaperf](https://llamaperf.com/leaderboard) - Community-reported leaderboard (medians).
- [LocalScore](https://github.com/cjpais/LocalScore) - Standardized single-GPU benchmark CLI.
- [canirun.ai](https://canirun.ai/) - Estimates whether and how fast a model fits your hardware.
- [awesome-local-llm](https://github.com/rafska/awesome-local-llm) - Directory of local LLM platforms and tools.
- [Awesome-LLM-Inference](https://github.com/xlite-dev/Awesome-LLM-Inference) - Inference papers with code.

## Contributing

<details><summary>Site preview</summary>

<img src="docs/screenshot.png" width="760" alt="RecipeBench">

</details>


One recipe = one PR. Copy the YAML template from [submit.html](submit.html), fill only what the source shows (`null` otherwise), run `node scripts/validate.mjs`, and link the post. Then run `python3 scripts/gen_readme.py` to regenerate this file. See [CONTRIBUTING.md](CONTRIBUTING.md).

Dev: `python3 -m http.server 5190` → `index.html` (landing) · `explore.html` (filter/sort/scatter) · schema in [`schema/recipe.schema.json`](schema/recipe.schema.json).

## License

Not chosen yet. Suggested: MIT for code, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) for `data/`.
