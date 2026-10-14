# Awesome Local Inference Recipes [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

> Model × engine × hardware → measured speed and cost, with every number linked to its source. Consumer and used hardware, up to $30k.

<sub>Working name: **RecipeBench** (placeholder) · 255 recipes (214 text · 16 image · 25 video/audio) · data as of 2026-10-13 · <a href="https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html">Explorer</a> · <a href="https://raytone-lab.github.io/Awesome-local-inference-recipe/submit.html">Submit</a></sub>

<sub>Site links point to GitHub Pages; if it is not live yet, clone the repo and open <code>explore.html</code> locally (<code>python3 -m http.server</code>).</sub>

**New:** step-by-step [recipe guides](recipes/README.md) · [Getting started](docs/getting-started.md)

## Contents

- [Legend](#legend)
- [Hot This Month](#hot-this-month)
- [Browse by Model Family](#browse-by-model-family)
- [Browse by Engine](#browse-by-engine)
- [Tier 1 · up to $2.5k](#tier-1--up-to-25k)
- [Tier 2 · $2.5k–7k](#tier-2--25k7k)
- [Tier 3 · $7k–14k](#tier-3--7k14k)
- [Tier 4 · $14k–30k](#tier-4--14k30k)
- [Cost Not Published](#cost-not-published)
- [Engines & Tools](#engines--tools)
- [Related Lists & Benchmarks](#related-lists--benchmarks)
- [License](#license)

## Legend

| Source level     | Meaning                               | Format                                                                  |
| ---------------- | ------------------------------------- | ----------------------------------------------------------------------- |
| 🏛️ **Official** | vendor or project number              | **Model** · Engine `quant` — Hardware → **key number** level \[source\] |
| ✅ **Measured**   | author ran it, with log or screenshot | **tok/s** = single-stream generation (not prefill, not aggregate)       |
| 🔁 **Relayed**   | second-hand, verify upstream          | Tiers use the lowest published hardware price (USD)                     |
| 📣 **Claimed**   | projection, no reproduction           | Unknown values are never estimated                                      |

## Hot This Month

Most-engaged recipe posts on X, 2026-09-15 → 10-13 (likes + 3×reposts).

- **MiniMax H3** · ComfyUI — RTX 5090 24GB + 64GB RAM → Three 5s chained clips: 17 min total ✅ [@EndFolding79421](https://x.com/EndFolding79421/status/2102448683245502844) ♥149
- **GLM 5.3** · oMLX — Mac Studio M5 Ultra → **87 tok/s** ✅ [@JamesMcPherson](https://x.com/JamesMcPherson/status/2104028051285672431) ♥106
- **Qwen3.8-Flash-Next** · Strata — AMD Strix Halo 395 → **47.7 tok/s** ✅ [@no_stp_on_snek](https://x.com/no_stp_on_snek/status/2108296174994088177) ♥73
- **Qwen3.8-Flash-Next** · Strata — RTX 5070 Ti 12GB + Intel 275HX + 64GB DDR5 + Gen4… → **51 tok/s** 🔁 [@jurlycat](https://x.com/jurlycat/status/2105165498967007621) ♥46
- **Qwen3.8-Flash-Next** · Strata — 2× RTX 3090 (48GB) + 64GB DDR5-6000 → **120 tok/s** ✅ [@geldeki](https://x.com/geldeki/status/2109208295957201171) ♥45
- **Qwen3.8-Flash-Next** — Mac Studio M5 Ultra → **85.9 tok/s** 🔁 [@wei_wang](https://x.com/wei_wang/status/2103459506944344323) ♥33
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s video + audio ≈72 s (steady state, excl. MP4 export; bas… 🏛️ [@LightX2V](https://x.com/LightX2V/status/2108769912009424976) ♥8
- **MiniMax H3** · TensorFold — RTX 5070 Ti 16GB + 64GB RAM → 1344×768 5s with audio: 81 s (stock ComfyUI, 20 steps: 623 s) ✅ [@jayleaton](https://x.com/jayleaton/status/2106213885917491367) ♥10

## Browse by Model Family

Click a family to open the explorer pre-filtered. Tags: [`dense`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=dense) 85, [`long-context`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=long-context) 81, [`speculative`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=speculative) 64, [`4bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=4bit) 58, [`MTP`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=MTP) 42, [`MoE`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=MoE) 33, [`3bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=3bit) 32, [`multi-GPU`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=multi-GPU) 32, [`2bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=2bit) 24, [`ternary`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=ternary) 22, [`8bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=8bit) 21, [`1bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=1bit) 12, [`few-step`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=few-step) 12, [`offload`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=offload) 11, [`bf16`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=bf16) 6, [`6bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=6bit) 6, [`abliterated`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=abliterated) 2, [`5bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=5bit) 1.

| Family                                                                                                      | Recipes | Text | Image | Video & Audio |
| ----------------------------------------------------------------------------------------------------------- | ------- | ---- | ----- | ------------- |
| [Qwen](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Qwen)               | 138     | 138  |       |               |
| [Bonsai](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Bonsai)           | 28      | 28   |       |               |
| [GLM](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=GLM)                 | 20      | 20   |       |               |
| [DeepSeek](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=DeepSeek)       | 18      | 18   |       |               |
| [MiniMax H3](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=MiniMax%20H3) | 17      |      |       | 17            |
| [Qwen-Image](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Qwen-Image)   | 13      |      | 13    |               |
| [LTX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=LTX)                 | 4       |      |       | 4             |
| [Z-Image](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Z-Image)         | 3       |      | 3     |               |
| [ACE-Step](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=ACE-Step)       | 2       |      |       | 2             |
| [Edge0](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Edge0)             | 2       | 2    |       |               |
| [Wan](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Wan)                 | 2       |      |       | 2             |
| [Other](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Other)             | 8       | 8    |       |               |

## Browse by Engine

Engine names are normalized (`scripts/normalize_engines.py`); original strings are kept in `engine_note`.

| Engine                                                                                                                                              | Recipes |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| [Strata](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Strata)                                                   | 29      |
| [llama.cpp](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp)                                             | 27      |
| [oMLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=oMLX)                                                       | 27      |
| [MLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX)                                                         | 16      |
| [TensorFold](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=TensorFold)                                           | 14      |
| [llama.cpp (PrismML fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28PrismML%20fork%29)       | 14      |
| [ComfyUI](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ComfyUI)                                                 | 12      |
| [MTPLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MTPLX)                                                     | 11      |
| [DFlash](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=DFlash)                                                   | 7       |
| [SGLang](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=SGLang)                                                   | 7       |
| [Splash](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Splash)                                                   | 5       |
| [mlx-serve](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mlx-serve)                                             | 5       |
| [Project Maya](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Project%20Maya)                                     | 4       |
| [mirai-s-ada](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mirai-s-ada)                                         | 4       |
| [ds4 (DwarfStar)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ds4%20%28DwarfStar%29)                           | 3       |
| [llama.cpp (agentionai fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28agentionai%20fork%29) | 3       |
| [vLLM](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=vLLM)                                                       | 3       |
| [Halogen](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Halogen)                                                 | 2       |
| [MLX Swift](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX%20Swift)                                           | 2       |
| [Ollama](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Ollama)                                                   | 2       |
| [Radiance (fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Radiance%20%28fork%29)                           | 2       |
| [edge0](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=edge0)                                                     | 2       |
| [DS41RT](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=DS41RT)                                                   | 1       |
| [ExLlama](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ExLlama)                                                 | 1       |
| [FreeToken](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=FreeToken)                                             | 1       |
| [LightX2V](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=LightX2V)                                               | 1       |
| [MLX Swift (PrismML fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX%20Swift%20%28PrismML%20fork%29)     | 1       |
| [NVIDIA Sol](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=NVIDIA%20Sol)                                         | 1       |
| [Osaurus](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Osaurus)                                                 | 1       |
| [TabbyAPI](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=TabbyAPI)                                               | 1       |
| [llama.cpp (mirai-s fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28mirai-s%20fork%29)       | 1       |
| [mflux](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mflux)                                                     | 1       |
| [sparkinfer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=sparkinfer)                                           | 1       |
| [Unspecified](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Unspecified)                                         | 43      |

## Tier 1 · up to $2.5k

*Used 3090/4090, MI50/V100 cards, Strix Halo, R9700* · 41 recipes


**📝 Text**

- **Bonsai-8B** · llama.cpp (PrismML fork) `1-bit Q1_0` — RTX 4090 → **368 tok/s** 📣 [source](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 4090 24GB → **225 tok/s** 📣 [source](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-Flash-Next** · Strata `Strata· Swift 1.5 IQ2_XS` — RTX 4090 24GB + 32GB DDR5 → **220 tok/s** ✅ [source](https://x.com/Knuckles_XBT/status/2105245662657011841)
- **Qwen3.6-35B-A3B** · FreeToken `FreeToken · NVFP4` — RTX 4090 → **167 tok/s** 🔁 [source](https://x.com/shipfrontierai/status/2092602493213577481)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 3090 24GB → **154 tok/s** 📣 [source](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-27B** · DFlash `DFlash2` — RTX 3090 24GB → **138 tok/s** 🔁 [source](https://x.com/yume_arasaki/status/2090971775714939097)
- **Bonsai-8B** · MLX `1-bit g128` — MacBook M4 Pro 48GB → **131 tok/s** 📣 [source](https://huggingface.co/prism-ml/Bonsai-8B-mlx-1bit)
- **Qwen3.8-27B** · DFlash `EXL3 4.0bpw + DFlash2 3-bit…` — RTX 4090 24GB → **121 tok/s** ✅ [source](https://x.com/yume_arasaki/status/2100595901006008791)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 3090 24GB → **120.8 tok/s** ✅ [source](https://x.com/needmorevram/status/2105050786938118599)
- **Qwen3.8-Flash-Next** · Strata `Q2_0` — AMD Radeon AI PRO R9700 → **100 tok/s** ✅ [source](https://x.com/TechPractice1/status/2105338176055509376) · [guide](recipes/x-009.md)
- *…and 23 more in the [explorer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html).*

**🖼️ Image**

- **Qwen-Image 2.1** · ComfyUI `Comfy-Org INT8 · ComfyUI` — RTX 4090 24GB → see source ✅ [source](https://x.com/yume_arasaki/status/2102176739359404499) · [guide](recipes/image-001.md)
- **Qwen-Image 2.1** `INT8` — RTX 3090 → see source 🔁 [source](https://x.com/yume_arasaki/status/2102176739359404499)
- **Qwen-Image 2.1** · ComfyUI `ComfyUI` — Mac M4 Pro → see source ✅ [source](https://x.com/gabeciii/status/2104920039077884324)
- **Z-Image Turbo** · ComfyUI `ComfyUI` — RTX 3090 24GB → see source ✅ [source](https://x.com/michaelricks/status/2104959036353356058)

**🎬 Video & Audio**

- **FastH3 V2 / Trim** `FP8` — RTX 4090 24GB → see source 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 4090 → see source ✅ [source](https://x.com/yume_arasaki/status/2097790831323427046)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 3090 → see source ✅ [source](https://x.com/natehalko/status/2103538997146611890)
- **ACE-Step 1.5** — RTX 3090 → see source 🔁 [source](https://x.com/simplifyinAI/status/2091935190335754493)

## Tier 2 · $2.5k–7k

*One RTX 5090, one DGX Spark, Mac Studio Max* · 75 recipes


**📝 Text**

- **Qwen3.6-35B-A3B** · sparkinfer `sparkinfer v0.4.4` — RTX 5090 → **512 tok/s** 📣 [source](https://x.com/kysstalol/status/2105042922643321008)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 5090 32GB → **283 tok/s** 📣 [source](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2) · [guide](recipes/hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.md)
- **Qwen3.6-35B-A3B** · DFlash `DFlash 2` — Mac Studio M3 Ultra → **251 tok/s** ✅ [source](https://x.com/tinybluedev/status/2089910202606764530)
- **Qwen3.8-Flash-Next** · Strata `IQ2_XS` — RTX 5090 + 256GB RAM → **176 tok/s** ✅ [source](https://x.com/TechPractice1/status/2105087037363884483)
- **Qwen3.8-27B** · llama.cpp `GPU-1+ DFlash2` — RTX 5090 32GB → **176 tok/s** 📣 [source](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- **Qwen3.8-27B** · llama.cpp `GPU-5+ DFlash2` — RTX 5090 32GB → **167 tok/s** 📣 [source](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090 → **160 tok/s** 🔁 [source](https://x.com/yume_arasaki/status/2107293459556225446)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090+ 96GB DDR5-6400 → **150 tok/s** 🔁 [source](https://x.com/kreia/status/2106054715373212025)
- **Qwen3.8-27B-NVFP4-MTP** · llama.cpp `LOW + MTP` — RTX 5090 32GB → **148.3 tok/s** 🔁 [source](https://huggingface.co/esatapedico/Qwen3.8-27B-NVFP4-MTP-GGUF)
- **Qwen3.8-Flash-Next-Gyro** · Strata `Gyro-S TQ1_0` — RTX 5090 32GB → **140 tok/s** 📣 [source](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF)
- *…and 47 more in the [explorer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html).*

**🖼️ Image**

- **Qwen-Image 2.1** `LightX2V / BennyDaBall NVFP…` — RTX 5090 32GB → see source 🔁 [source](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image 2.1** · TensorFold `TensorFold NVFP4 / FP8 / GG…` — RTX 5090 @450W → see source ✅ [source](https://x.com/niklaslenz_ai/status/2106465941177487871)
- **Qwen-Image 2.1** — RTX 5090 → see source 📣 [source](https://x.com/fractalyze_io/status/2105207217452695841)
- **Qwen-Image 2.1** · SGLang `spark-image-lab BF16 / SGLa…` — 1× DGX Spark → see source 🔁 [source](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image-2.1-Turbo** `Turbo 8 vs Base 40` — RTX 5090 → see source ✅ [source](https://x.com/niklaslenz_ai/status/2108609693941920176)
- **Z-Image Turbo vs Qwen-Image 2.1** `prompt seed 20` — RTX 5090 → see source ✅ [source](https://x.com/princedoesai/status/2109376490009743713)

**🎬 Video & Audio**

- **FastH3 V2** `NVFP4` — RTX 5090 32GB → see source 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/) · [guide](recipes/video-audio-001.md)
- **FastH3 Trim** `NVFP4` — RTX 5090 → see source 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/)
- **FastH3 V2 / Trim** `NVFP4` — 1× / 2× DGX Spark → see source 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3** · ComfyUI `ComfyUI + SageAttention` — RTX 5090 → see source ✅ [source](https://x.com/RKAScope/status/2084359480926503182)
- **MiniMax H3 vs FastH3 Turbo** `seed` — RTX 5090 → see source ✅ [source](https://x.com/Sogni_Protocol/status/2097254959729246550)
- **MiniMax H3** · NVIDIA Sol `NVIDIA Sol` — 1× DGX Spark → see source ✅ [source](https://x.com/yume_arasaki/status/2100734364908986511)
- **MiniMax H3 vs LTX-2.3 Eros** `3 prompt` — 1× DGX Spark → see source ✅ [source](https://x.com/YRSM_Simon/status/2084222856972456336)
- **LTX-2.3** · ComfyUI `ComfyUI` — RTX 5090 → see source ✅ [source](https://x.com/freshstartsnow/status/2092263835591655773)
- **LTX-2.5** `LoRA` — RTX 5090 → see source ✅ [source](https://x.com/PhotogenicWeekE/status/2087298681137701274)
- **ACE-Step 1.5 + LTX-2.3** · ComfyUI `ComfyUI` — 1× DGX Spark → see source 🔁 [source](https://x.com/yume_arasaki/status/2100734364908986511)
- **Wan2.1 14B** `97% + 3 + FP8` — RTX 5090 → see source 📣 [source](https://x.com/thePandaily/status/2105209996648567243)
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s video + audio ≈72 s (steady state, excl. MP4 export; bas… 🏛️ [source](https://x.com/LightX2V/status/2108769912009424976)

## Tier 3 · $7k–14k

*Two Sparks, Mac Studio Ultra* · 15 recipes


**📝 Text**

- **Qwen3.8-Flash-Next** · TensorFold `TensorFold · NVFP4 / INT4-A…` — 2× DGX Spark → **67.4 tok/s** 🔁 [source](https://x.com/llm_frontier_jp/status/2108884169069916440)
- **GLM-5.3-Flash** · TensorFold — 2× DGX Spark → **54 tok/s** ✅ [source](https://x.com/easthambuilds/status/2105693180427452703)
- **DeepSeek-V4.1-Flash** `Mia EXL3 2.9bpw · DSpark k=3` — 2× DGX Spark → **48.5 tok/s** ✅ [source](https://x.com/yume_arasaki/status/2099966865326170554)
- **GLM-5.3-Flash** — 2× DGX Spark → **30 tok/s** ✅ [source](https://x.com/realWeZZard/status/2099322375770869891)
- **Qwen3.8-Flash-Next** · vLLM `vr8vr8 v4.1` — 2× DGX Spark → see source ✅ [source](https://x.com/yume_arasaki/status/2104582876956332408)
- **Qwen3.8-Flash-Next** · oMLX `fused-kernel oMLX` — Mac Studio M3 Ultra 256GB → see source 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- **Qwen3.8-Flash-Next** · oMLX `oMLX / TensorFold` — Mac Studio M5 Ultra 80C 256GB → see source 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- **Qwen3.8-27B** · TensorFold `TensorFold 1.0.7` — Mac Studio M3 Ultra → see source 🏛️ [source](https://x.com/VRAMCalculator/status/2109344267994808619)
- **GLM-5.3-Flash** · TensorFold `Mia EXL3 + TensorFold` — 2× DGX Spark → see source ✅ [source](https://x.com/yume_arasaki/status/2106837882870886438)
- **GLM-5.3-Flash** `@Morrowmake` — 4× CMP 170HX 64GB → see source ✅ [source](https://x.com/seanphan/status/2105673568914898962)
- *…and 5 more in the [explorer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html).*

## Tier 4 · $14k–30k

*3–4 Spark clusters, multi-GPU workstations* · 8 recipes


**📝 Text**

- **Qwen3.8-Flash-Next** · Radiance (fork) `Radiance fork · int4fp8 · B…` — 4× AMD R9700 32GB + TR 9970X + 128GB → see source 🔁 [source](https://x.com/richgel999/status/2109515169638326738)
- **Qwen3.8-27B** · Radiance (fork) `MXFP4 · Radiance fork` — 4× R9700 → see source 🔁 [source](https://x.com/richgel999/status/2109515169638326738)
- **GLM-5.3-Flash** `Mia EXL3` — 3× DGX Spark → see source 🔁 [source](https://x.com/yume_arasaki/status/2106837882870886438)
- **GLM-5.3-Flash** · TensorFold `TensorFold · Thunderbolt 5×…` — 2× Mac Studio M5 Ultra → see source 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- **DeepSeek-V4.1-Flash** `Mia MXFP4/FP8 · Engram NVMe` — 3× DGX Spark → see source 🔁 [source](https://x.com/yume_arasaki/status/2099966865326170554)
- **DeepSeek-V4.1-Flash** · TensorFold `tonyd615 MXFP4 / Mia Tensor…` — 4× DGX Spark → see source 🔁 [source](https://x.com/yume_arasaki/status/2106837882870886438)
- **DeepSeek-V4.1-Flash** — 4× DGX Spark → see source 🔁 [source](https://x.com/hardfanaticos/status/2107225102475813374)
- **DeepSeek-V4.1-Flash** · MLX `MLX Q4i / DwarfStar` — M3 Ultra 512GB / M5 Max 128GB → see source 🔁 [source](https://x.com/yume_arasaki/status/2099966865326170554)

## Cost Not Published

Multi-card builds priced per card, Macs without a listed price, and other rows without a single published price · 116 recipes. Top text recipes by tok/s:

- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 5080 16GB → **212 tok/s** 📣 [source](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.6-35B-A3B** · Splash `Splash` — Mac M5 Pro 48GB → **210 tok/s** 🔁 [source](https://x.com/TeksEdge/status/2101735798567764421)
- **Qwen3.6-35B-A3B** · oMLX `oMLX 0.7.1.dev1` — Mac M5 Max → **205 tok/s** 🏛️ [source](https://x.com/jundotkim/status/2108584837590495246)
- **Qwen3.8-Flash-Next-MLX-Serve-iQ-MLX-4.7bpw** · mlx-serve `iQ-MLX 4.7 bpw` — Mac Studio M5 Ultra → **157 tok/s** 📣 [source](https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-iQ-MLX-4.7bpw)
- **Qwen3.8-27B** · vLLM `vLLM` — CMP 170HX → **147 tok/s** 🔁 [source](https://x.com/LFrefman/status/2101572845017178243)
- **Qwen3.8-27B** · Splash `Splash` — Mac M5 Max → **144 tok/s** 🏛️ [source](https://x.com/zhijianliu/status/2101102949158302001)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 5060 Ti 16GB → **128 tok/s** 📣 [source](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **GLM-5.3-Flash** `EXL3+ DS coordinator` — 4× DGX Spark + RTX 5090 → **124 tok/s** ✅ [source](https://x.com/dangerm00se/status/2104876537367728325)
- **Qwen3.8-Flash-Next** · Strata `IQ3_S` — 2× RTX 3090 (48GB) + 64GB DDR5-6000 → **120 tok/s** ✅ [source](https://x.com/geldeki/status/2109208295957201171) · [guide](recipes/x-004.md)
- **Qwen3.8-Flash-Next** · Strata `q3 xs` — 2× Tesla V100 32GB PCIe → **120 tok/s** ✅ [source](https://x.com/rewin123/status/2108669905616736529) · [guide](recipes/x-007.md)
- **Ternary-Bonsai-2-27B-262k** · mirai-s-ada `Ternary Bonsai 2 27B + KV` — RTX 4070 12GB → **102 tok/s** 📣 [source](https://huggingface.co/CaryPalmer/Ternary-Bonsai-2-27B-262k-GGUF)
- **Qwen3.8-Flash-Next** · Strata `Strata · Q2_0` — RTX 5070 12GB + Ryzen 5 7600 + 64GB DDR5 → **94 tok/s** 🏛️ [source](https://github.com/Niko1221/Strata)
- *…browse all 116 in the [explorer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html).*


## Engines & Tools

| Project                                                       | ⭐ Stars | Live                                                                                            | Last push  | What                                                                                                    |
| ------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------- |
| [llama.cpp](https://github.com/ggml-org/llama.cpp)            | 131.0k  | ![stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat&label=)              | 2026-10-13 | The baseline GGUF engine (CPU/CUDA/ROCm/Vulkan/Metal).                                                  |
| [vLLM](https://github.com/vllm-project/vllm)                  | 93.7k   | ![stars](https://img.shields.io/github/stars/vllm-project/vllm?style=flat&label=)               | 2026-10-13 | High-throughput server; MTP and multi-stream recipes on Spark.                                          |
| [SGLang](https://github.com/sgl-project/sglang)               | 37.1k   | ![stars](https://img.shields.io/github/stars/sgl-project/sglang?style=flat&label=)              | 2026-10-13 | Serving framework; paired with DFlash2 on DGX Spark.                                                    |
| [MLX](https://github.com/ml-explore/mlx)                      | 28.8k   | ![stars](https://img.shields.io/github/stars/ml-explore/mlx?style=flat&label=)                  | 2026-10-13 | Apple's array framework behind most Mac recipes.                                                        |
| [Strata](https://github.com/Niko1221/Strata)                  | 23.5k   | ![stars](https://img.shields.io/github/stars/Niko1221/Strata?style=flat&label=)                 | 2026-10-12 | MoE engine that splits experts across GPU, RAM and SSD for 12–24GB cards; most Flash-Next recipes here. |
| [oMLX](https://github.com/jundot/omlx)                        | 22.8k   | ![stars](https://img.shields.io/github/stars/jundot/omlx?style=flat&label=)                     | 2026-10-13 | Apple Silicon MLX server with continuous batching and tiered KV/SSD cache.                              |
| [DFlash / DFlash 2](https://github.com/z-lab/dflash)          | 6.2k    | ![stars](https://img.shields.io/github/stars/z-lab/dflash?style=flat&label=)                    | 2026-08-18 | Block-diffusion speculative decoding; DFlash 2 drafts for Qwen3.8-27B.                                  |
| [LightX2V](https://github.com/ModelTC/LightX2V)               | 2.9k    | ![stars](https://img.shields.io/github/stars/ModelTC/LightX2V?style=flat&label=)                | 2026-10-13 | Video generation inference framework; MiniMax H3 results on a 5090.                                     |
| [TensorFold](https://github.com/ashhart/TensorFold)           | 1.3k    | ![stars](https://img.shields.io/github/stars/ashhart/TensorFold?style=flat&label=)              | 2026-10-12 | OpenAI-compatible MoE runtime with speculative decoding; also used for MiniMax H3 in ComfyUI.           |
| [halogen](https://github.com/peonist-ai/halogen-flash-server) | 954     | ![stars](https://img.shields.io/github/stars/peonist-ai/halogen-flash-server?style=flat&label=) | 2026-10-13 | Flash-Next server tuned for Strix Halo.                                                                 |
| [dflash-mlx](https://github.com/bstnxbt/dflash-mlx)           | 788     | ![stars](https://img.shields.io/github/stars/bstnxbt/dflash-mlx?style=flat&label=)              | 2026-08-20 | DFlash speculative decoding for MLX on Apple Silicon.                                                   |
| [FastH3](https://haoailab.com/blogs/fasth3-rtx/)              | —       | *(site/blog)*                                                                                   | —          | Hao AI Lab's 8-step distilled MiniMax H3 for RTX cards (blog).                                          |

<sub>⭐ Snapshot updated 2026-10-13T14:44Z (UTC) by `scripts/update_stars.py` · *Live* badges are rendered by shields.io at view time.</sub>

## Related Lists & Benchmarks

| Project                                                                     | ⭐ Stars | Live                                                                                            | Last push  | What                                                       |
| --------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------- |
| [Awesome-LLM-Inference](https://github.com/xlite-dev/Awesome-LLM-Inference) | 5.5k    | ![stars](https://img.shields.io/github/stars/xlite-dev/Awesome-LLM-Inference?style=flat&label=) | 2026-08-14 | Inference papers with code.                                |
| [awesome-local-llm](https://github.com/rafska/awesome-local-llm)            | 3.0k    | ![stars](https://img.shields.io/github/stars/rafska/awesome-local-llm?style=flat&label=)        | 2026-10-12 | Directory of local LLM platforms and tools.                |
| [LocalScore](https://github.com/cjpais/LocalScore)                          | 134     | ![stars](https://img.shields.io/github/stars/cjpais/LocalScore?style=flat&label=)               | 2026-10-09 | Standardized single-GPU benchmark CLI.                     |
| [llamabench.ai](https://llamabench.ai/)                                     | —       | *(site/blog)*                                                                                   | —          | llama.cpp results with full launch commands.               |
| [llamaperf](https://llamaperf.com/leaderboard)                              | —       | *(site/blog)*                                                                                   | —          | Community-reported leaderboard (medians).                  |
| [canirun.ai](https://canirun.ai/)                                           | —       | *(site/blog)*                                                                                   | —          | Estimates whether and how fast a model fits your hardware. |

<sub>⭐ Snapshot updated 2026-10-13T14:44Z (UTC) by `scripts/update_stars.py` · *Live* badges are rendered by shields.io at view time.</sub>

## Contributing

One recipe = one PR. Copy the YAML template from [submit.html](https://raytone-lab.github.io/Awesome-local-inference-recipe/submit.html), fill only what the source shows (`null` otherwise), run `node scripts/validate.mjs`, and link the post. Then run `python3 scripts/gen_readme.py` to regenerate all READMEs. See [CONTRIBUTING.md](CONTRIBUTING.md).

Dev: `python3 -m http.server 5190` → `index.html` (landing) · `explore.html` (filter/sort/scatter) · schema in [`schema/recipe.schema.json`](schema/recipe.schema.json).

<details><summary>Site preview</summary>

<img src="docs/screenshot.png" width="760" alt="RecipeBench">

</details>

## License

- Code: [MIT](LICENSE)
- Data (`data/`): [CC BY 4.0](LICENSE-DATA). Reuse it freely with attribution to RecipeBench and the original sources linked in each recipe.
