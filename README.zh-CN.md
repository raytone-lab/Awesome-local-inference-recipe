# 本地推理配方精选 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](README.md) | **简体中文**

> 模型 × 引擎 × 硬件 → 实测速度与成本，每个数字都链接到来源。聚焦消费级与二手硬件，预算 3 万美元以内。

<sub>暂定名：**RecipeBench** · 共 255 条配方（文字 214 · 图像 16 · 影音 25）· 数据截至 2026-10-13 · <a href="https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html">配方库</a> · <a href="https://raytone-lab.github.io/Awesome-local-inference-recipe/submit.html">提交配方</a></sub>

<sub>站内链接指向 GitHub Pages；若尚未上线，可克隆仓库后在本地打开 <code>explore.html</code>（<code>python3 -m http.server</code>）。</sub>

**新增：** 分步 [配方指南](recipes/README.zh-CN.md) · [入门指南](docs/getting-started.zh-CN.md)

## 目录

- [图例](#图例)
- [本月热门](#本月热门)
- [按模型系列浏览](#按模型系列浏览)
- [按引擎浏览](#按引擎浏览)
- [第 1 档 · 2,500 美元以内](#第-1-档--2500-美元以内)
- [第 2 档 · 2,500–7,000 美元](#第-2-档--25007000-美元)
- [第 3 档 · 7,000–14,000 美元](#第-3-档--700014000-美元)
- [第 4 档 · 14,000–30,000 美元](#第-4-档--1400030000-美元)
- [价格未公开](#价格未公开)
- [引擎与工具](#引擎与工具)
- [相关榜单与清单](#相关榜单与清单)
- [参与贡献](#参与贡献)
- [许可证](#许可证)

## 图例

| 来源等级 | 含义 | 格式 |
|---|---|---|
| 🏛️ **官方** | 项目方或厂商发布的数字 | **模型** · 引擎 `量化` — 硬件 → **关键数字** 等级 [来源] |
| ✅ **实测** | 作者本人跑出，附日志或截图 | **tok/s** 指单路生成速度（不含读入，不含多路合计） |
| 🔁 **转述** | 二手引用，请回原帖核对 | 预算档按公开的最低硬件价格（美元）划分 |
| 📣 **宣称** | 预测值，无复现条件 | 未知字段一律不估算，显示「未见公开数据」 |

## 本月热门

X 上互动最多的配方帖，2026-09-15 至 10-13（按 点赞 + 3×转发 排序）。

- **MiniMax H3** · ComfyUI — 笔记本 RTX 5090 24GB + 64GB RAM → 3 段 5s 衔接片段共 17 分钟 ✅ [@EndFolding79421](https://x.com/EndFolding79421/status/2102448683245502844) ♥149
- **GLM 5.3（帖文原话 “GLM 5.3 Code”）** · oMLX — Mac Studio M5 Ultra → **87 tok/s** ✅ [@JamesMcPherson](https://x.com/JamesMcPherson/status/2104028051285672431) ♥106
- **Qwen3.8-Flash-Next** · Strata — AMD Strix Halo 395 → **47.7 tok/s** ✅ [@no_stp_on_snek](https://x.com/no_stp_on_snek/status/2108296174994088177) ♥73
- **Qwen3.8-Flash-Next** · Strata — 笔记本 RTX 5070 Ti 12GB + Intel 275HX + 64GB DDR5 + … → **51 tok/s** 🔁 [@jurlycat](https://x.com/jurlycat/status/2105165498967007621) ♥46
- **Qwen3.8-Flash-Next** · Strata — 2× RTX 3090 (48GB) + 64GB DDR5-6000 → **120 tok/s** ✅ [@geldeki](https://x.com/geldeki/status/2109208295957201171) ♥45
- **Qwen3.8-Flash-Next** — Mac Studio M5 Ultra → **85.9 tok/s** 🔁 [@wei_wang](https://x.com/wei_wang/status/2103459506944344323) ♥33
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s 视频+音频 ≈72 s（稳态，不含 MP4 导出；基线 ~26 分钟） 🏛️ [@LightX2V](https://x.com/LightX2V/status/2108769912009424976) ♥8
- **MiniMax H3** · TensorFold — RTX 5070 Ti 16GB + 64GB RAM（Windows） → 1344×768 5s 带声音：81 s（原生 ComfyUI 20 步 623 s） ✅ [@jayleaton](https://x.com/jayleaton/status/2106213885917491367) ♥10

## 按模型系列浏览

点击系列名即可打开已筛选的配方库。标签：[`dense`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=dense) 85, [`long-context`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=long-context) 81, [`speculative`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=speculative) 64, [`4bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=4bit) 58, [`MTP`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=MTP) 42, [`MoE`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=MoE) 33, [`3bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=3bit) 32, [`multi-GPU`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=multi-GPU) 32, [`2bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=2bit) 24, [`ternary`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=ternary) 22, [`8bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=8bit) 21, [`1bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=1bit) 12, [`few-step`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=few-step) 12, [`offload`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=offload) 11, [`bf16`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=bf16) 6, [`6bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=6bit) 6, [`abliterated`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=abliterated) 2, [`5bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=5bit) 1。

| 系列 | 配方数 | 文字 | 图像 | 影音 |
|---|--:|--:|--:|--:|
| [Qwen](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Qwen) | 138 | 138 |  |  |
| [Bonsai](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Bonsai) | 28 | 28 |  |  |
| [GLM](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=GLM) | 20 | 20 |  |  |
| [DeepSeek](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=DeepSeek) | 18 | 18 |  |  |
| [MiniMax H3](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=MiniMax%20H3) | 17 |  |  | 17 |
| [Qwen-Image](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Qwen-Image) | 13 |  | 13 |  |
| [LTX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=LTX) | 4 |  |  | 4 |
| [Z-Image](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Z-Image) | 3 |  | 3 |  |
| [ACE-Step](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=ACE-Step) | 2 |  |  | 2 |
| [Edge0](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Edge0) | 2 | 2 |  |  |
| [Wan](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Wan) | 2 |  |  | 2 |
| [Other](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Other) | 8 | 8 |  |  |

## 按引擎浏览

引擎名已统一（`scripts/normalize_engines.py`），原始写法保留在 `engine_note` 字段。

| 引擎 | 配方数 |
|---|--:|
| [Strata](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Strata) | 29 |
| [llama.cpp](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp) | 27 |
| [oMLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=oMLX) | 27 |
| [MLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX) | 16 |
| [TensorFold](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=TensorFold) | 14 |
| [llama.cpp (PrismML fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28PrismML%20fork%29) | 14 |
| [ComfyUI](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ComfyUI) | 12 |
| [MTPLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MTPLX) | 11 |
| [DFlash](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=DFlash) | 7 |
| [SGLang](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=SGLang) | 7 |
| [Splash](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Splash) | 5 |
| [mlx-serve](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mlx-serve) | 5 |
| [Project Maya](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Project%20Maya) | 4 |
| [mirai-s-ada](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mirai-s-ada) | 4 |
| [ds4 (DwarfStar)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ds4%20%28DwarfStar%29) | 3 |
| [llama.cpp (agentionai fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28agentionai%20fork%29) | 3 |
| [vLLM](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=vLLM) | 3 |
| [Halogen](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Halogen) | 2 |
| [MLX Swift](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX%20Swift) | 2 |
| [Ollama](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Ollama) | 2 |
| [Radiance (fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Radiance%20%28fork%29) | 2 |
| [edge0](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=edge0) | 2 |
| [DS41RT](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=DS41RT) | 1 |
| [ExLlama](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ExLlama) | 1 |
| [FreeToken](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=FreeToken) | 1 |
| [LightX2V](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=LightX2V) | 1 |
| [MLX Swift (PrismML fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX%20Swift%20%28PrismML%20fork%29) | 1 |
| [NVIDIA Sol](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=NVIDIA%20Sol) | 1 |
| [Osaurus](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Osaurus) | 1 |
| [TabbyAPI](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=TabbyAPI) | 1 |
| [llama.cpp (mirai-s fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28mirai-s%20fork%29) | 1 |
| [mflux](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mflux) | 1 |
| [sparkinfer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=sparkinfer) | 1 |
| [Unspecified](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Unspecified) | 43 |

## 第 1 档 · 2,500 美元以内

*二手 3090/4090、MI50/V100、Strix Halo、R9700* · 共 41 条


**📝 文字**

- **Bonsai-8B** · llama.cpp (PrismML fork) `1-bit Q1_0` — RTX 4090 → **368 tok/s** 📣 [来源](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 4090 24GB → **225 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-Flash-Next** · Strata `Strata（作者自改版）· Swift 1.5 IQ…` — RTX 4090 24GB + 32GB DDR5 → **220 tok/s** ✅ [来源](https://x.com/Knuckles_XBT/status/2105245662657011841)
- **Qwen3.6-35B-A3B** · FreeToken `FreeToken · NVFP4（无投机）` — RTX 4090 → **167 tok/s** 🔁 [来源](https://x.com/shipfrontierai/status/2092602493213577481)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 3090 24GB → **154 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-27B** · DFlash `DFlash2（TeksEdge）` — RTX 3090 24GB → **138 tok/s** 🔁 [来源](https://x.com/yume_arasaki/status/2090971775714939097)
- **Bonsai-8B** · MLX `1-bit g128` — MacBook M4 Pro 48GB → **131 tok/s** 📣 [来源](https://huggingface.co/prism-ml/Bonsai-8B-mlx-1bit)
- **Qwen3.8-27B** · DFlash `EXL3 4.0bpw + DFlash2 草稿（r0…` — RTX 4090 24GB → **121 tok/s** ✅ [来源](https://x.com/yume_arasaki/status/2100595901006008791)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S（GSQ-RCO）` — 单 RTX 3090 24GB（+64GB RAM 同作者前帖） → **120.8 tok/s** ✅ [来源](https://x.com/needmorevram/status/2105050786938118599)
- **Qwen3.8-Flash-Next** · Strata `Q2_0` — AMD Radeon AI PRO R9700 → **100 tok/s** ✅ [来源](https://x.com/TechPractice1/status/2105338176055509376) · [指南](recipes/x-009.zh-CN.md)
- *……另有 23 条，见 [配方库](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)。*

**🖼️ 图像**

- **Qwen-Image 2.1（7B + 8B 文本编码器）** · ComfyUI `官方 Comfy-Org INT8 · ComfyUI` — RTX 4090 24GB → 8.1 s / 1024²（40 步）；30.2 s / 2048×1152（50 步）；峰值 16.2GB ✅ [来源](https://x.com/yume_arasaki/status/2102176739359404499) · [指南](recipes/image-001.zh-CN.md)
- **Qwen-Image 2.1** `INT8` — RTX 3090 → 82–96 s / 2K（公开回执） 🔁 [来源](https://x.com/yume_arasaki/status/2102176739359404499)
- **Qwen-Image 2.1（编辑）** · ComfyUI `ComfyUI` — Mac M4 Pro → 3 分 52 秒 / 张（768 编辑） ✅ [来源](https://x.com/gabeciii/status/2104920039077884324)
- **Z-Image Turbo（6B，8 步）** · ComfyUI `ComfyUI` — RTX 3090 24GB → 2048px 约 8 s / 张；另一用户预热后 12 s ✅ [来源](https://x.com/michaelricks/status/2104959036353356058)

**🎬 影音**

- **FastH3 V2 / Trim** `FP8` — RTX 4090 24GB → 480p 5s：54.6 / 43.9 s；768p：154.6 / 132.8 s；8GB 限制 Trim 82.0 s 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3（turbo）** · ComfyUI `ComfyUI` — RTX 4090 → 5 s 片段 ~91 s；15 s ~8 分钟；960×544×5s 约 50 s ✅ [来源](https://x.com/yume_arasaki/status/2097790831323427046)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 3090 → 11 s 视频 13 分钟 ✅ [来源](https://x.com/natehalko/status/2103538997146611890)
- **ACE-Step 1.5（音乐）** — RTX 3090 → 整首歌 <10 s（宣传帖） 🔁 [来源](https://x.com/simplifyinAI/status/2091935190335754493)

## 第 2 档 · 2,500–7,000 美元

*单张 RTX 5090、单台 DGX Spark、Mac Studio Max* · 共 75 条


**📝 文字**

- **Qwen3.6-35B-A3B** · sparkinfer `sparkinfer v0.4.4（Blackwell…` — RTX 5090 → **512 tok/s** 📣 [来源](https://x.com/kysstalol/status/2105042922643321008)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2（INT8=on）` — RTX 5090 32GB → **283 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2) · [指南](recipes/hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.zh-CN.md)
- **Qwen3.6-35B-A3B** · DFlash `DFlash 2` — Mac Studio M3 Ultra → **251 tok/s** ✅ [来源](https://x.com/tinybluedev/status/2089910202606764530)
- **Qwen3.8-Flash-Next** · Strata `IQ2_XS` — RTX 5090 + 256GB RAM → **176 tok/s** ✅ [来源](https://x.com/TechPractice1/status/2105087037363884483)
- **Qwen3.8-27B** · llama.cpp `GPU-1（2.56 bpw）+ DFlash2（7 …` — RTX 5090 32GB → **176 tok/s** 📣 [来源](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- **Qwen3.8-27B** · llama.cpp `GPU-5（3.84 bpw）+ DFlash2（7 …` — RTX 5090 32GB → **167 tok/s** 📣 [来源](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090（RAM 未注明） → **160 tok/s** 🔁 [来源](https://x.com/yume_arasaki/status/2107293459556225446)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090（功耗限制）+ 96GB DDR5-6400 → **150 tok/s** 🔁 [来源](https://x.com/kreia/status/2106054715373212025)
- **Qwen3.8-27B-NVFP4-MTP** · llama.cpp `LOW + MTP（--spec-draft-n-ma…` — RTX 5090 32GB → **148.3 tok/s** 🔁 [来源](https://huggingface.co/esatapedico/Qwen3.8-27B-NVFP4-MTP-GGUF)
- **Qwen3.8-Flash-Next-Gyro** · Strata `Gyro-S TQ1_0（27.64 GiB）` — RTX 5090 32GB → **140 tok/s** 📣 [来源](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF)
- *……另有 47 条，见 [配方库](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)。*

**🖼️ 图像**

- **Qwen-Image 2.1** `LightX2V / BennyDaBall NVFP…` — RTX 5090 32GB → 5.93 s；NVFP4 6.7 s vs INT8 7.6 s vs BF16 15.6 s（1024²） 🔁 [来源](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image 2.1** · TensorFold `TensorFold NVFP4 / FP8 / GG…` — RTX 5090 @450W → 4.53 s / 6.94 s / 13.87 s（1024²，25 步；NVFP4 峰值 22.9GB；图像与 Q6 不完全一致） ✅ [来源](https://x.com/niklaslenz_ai/status/2106465941177487871)
- **Qwen-Image 2.1** `厂商内核重写+步缓存` — RTX 5090 → 13.5 s → 1.9 s / 张（厂商宣称） 📣 [来源](https://x.com/fractalyze_io/status/2105207217452695841)
- **Qwen-Image 2.1** · SGLang `spark-image-lab BF16 / SGLa…` — 1× DGX Spark（对照 4090） → 52.6 s / 1024²；SGLang 表：Spark 35.4 s，4090 18.7 s 🔁 [来源](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image-2.1-Turbo（官方 8 步）** `Turbo 8 步 vs Base 40 步` — RTX 5090 → 29 s vs 108 s / 张（2048²） ✅ [来源](https://x.com/niklaslenz_ai/status/2108609693941920176)
- **Z-Image Turbo vs Qwen-Image 2.1** `同 prompt 同 seed 20 轮` — RTX 5090 → Z-Image 快约 2×（无绝对时间）；质量 Qwen 9:6 胜 ✅ [来源](https://x.com/princedoesai/status/2109376490009743713)

**🎬 影音**

- **FastH3 V2（MiniMax H3 8 步蒸馏）** `NVFP4` — RTX 5090 32GB → 832×480×5s：14.8 s；1344×768×5s：38.6 s（含音频，端到端） 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/) · [指南](recipes/video-audio-001.zh-CN.md)
- **FastH3 Trim（42 块剪枝，实验）** `NVFP4` — RTX 5090 → 480p 5s：13.4 s；768p：35.4 s 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/)
- **FastH3 V2 / Trim** `NVFP4` — 1× / 2× DGX Spark → 1×：480p 141.4 / 125.8 s，Trim 768p 340.1 s；2×：87.2 / 78.3 s 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3（基础，50 步类）** · ComfyUI `ComfyUI + SageAttention` — RTX 5090 → 1280×736×5s：242 s → 168 s ✅ [来源](https://x.com/RKAScope/status/2084359480926503182)
- **MiniMax H3 vs FastH3 Turbo** `同图同 seed` — RTX 5090 → 15 s 片段：11 分 55 秒 vs 2 分 6 秒 ✅ [来源](https://x.com/Sogni_Protocol/status/2097254959729246550)
- **MiniMax H3（Sol 加速 / 无加速）** · NVIDIA Sol `NVIDIA Sol 引擎` — 1× DGX Spark → Sol：480p 5 s 约 68 s（NVIDIA 公布 56 s）；无 Sol >400 s；无 Sol 720p 20 步：5 s … ✅ [来源](https://x.com/yume_arasaki/status/2100734364908986511)
- **MiniMax H3 vs LTX-2.3 Eros** `同条件 3 组 prompt` — 1× DGX Spark → 864×480×5s：H3 平均 270 s；LTX 154 s（快 1.76×） ✅ [来源](https://x.com/YRSM_Simon/status/2084222856972456336)
- **LTX-2.3（带口型同步）** · ComfyUI `ComfyUI` — RTX 5090 → 10 s 约 90 s（较弱 GPU 约 6×） ✅ [来源](https://x.com/freshstartsnow/status/2092263835591655773)
- **LTX-2.5（t2v）** `模板 + LoRA` — RTX 5090（500W） → 720p/10 s：61.11 s；1080p/10 s：189.90 s ✅ [来源](https://x.com/PhotogenicWeekE/status/2087298681137701274)
- **ACE-Step 1.5 + LTX-2.3** · ComfyUI `ComfyUI 串行工作流` — 1× DGX Spark → 2 分 05 秒歌曲一次生成；+2:28 口型视频端到端 32 分钟 🔁 [来源](https://x.com/yume_arasaki/status/2100734364908986511)
- **Wan2.1 14B（SparkDiffusion）** `97% 稀疏注意力 + 3 步蒸馏 + FP8` — RTX 5090 → 720p：4,769 s → 18 s（项目宣称 265×） 📣 [来源](https://x.com/thePandaily/status/2105209996648567243)
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s 视频+音频 ≈72 s（稳态，不含 MP4 导出；基线 ~26 分钟） 🏛️ [来源](https://x.com/LightX2V/status/2108769912009424976)

## 第 3 档 · 7,000–14,000 美元

*双 Spark、Mac Studio Ultra* · 共 15 条


**📝 文字**

- **Qwen3.8-Flash-Next** · TensorFold `TensorFold · NVFP4 全模型 / IN…` — 2× DGX Spark → **67.4 tok/s** 🔁 [来源](https://x.com/llm_frontier_jp/status/2108884169069916440)
- **GLM-5.3-Flash** · TensorFold — 2× DGX Spark（TP2） → **54 tok/s** ✅ [来源](https://x.com/easthambuilds/status/2105693180427452703)
- **DeepSeek-V4.1-Flash** `Mia EXL3 2.9bpw · DSpark k=…` — 2× DGX Spark → **48.5 tok/s** ✅ [来源](https://x.com/yume_arasaki/status/2099966865326170554)
- **GLM-5.3-Flash** `未注明` — 2× DGX Spark → **30 tok/s** ✅ [来源](https://x.com/realWeZZard/status/2099322375770869891)
- **Qwen3.8-Flash-Next** · vLLM `vr8vr8 v4.1 配方（vLLM，TP=2）` — 2× DGX Spark → 散文 81.6；结构化 138.3；代码 133.2；4 流结构化合计 383.1 ✅ [来源](https://x.com/yume_arasaki/status/2104582876956332408)
- **Qwen3.8-Flash-Next** · oMLX `fused-kernel oMLX 分支` — Mac Studio M3 Ultra 256GB → 102 单流；8 流 134（stock oMLX 25） 🔁 [来源](https://x.com/yume_arasaki/status/2108359576966094952)
- **Qwen3.8-Flash-Next** · oMLX `调优 oMLX / TensorFold` — Mac Studio M5 Ultra 80C 256GB → oMLX 157.7（195K 时 96.6）；TensorFold 200.7 解码但仅 471 PP（oMLX 3,300–3,600） 🔁 [来源](https://x.com/yume_arasaki/status/2108359576966094952)
- **Qwen3.8-27B** · TensorFold `TensorFold 1.0.7（采样模式也可起草）` — Mac Studio M3 Ultra → 代码 125；散文 51（1.0.5 约 20） 🏛️ [来源](https://x.com/VRAMCalculator/status/2109344267994808619)
- **GLM-5.3-Flash** · TensorFold `Mia EXL3 + TensorFold（TP=2）` — 2× DGX Spark → 散文 60.4；结构化 114.7；4 流合计 108.8；8K 54.9 → 874K 44.6 ✅ [来源](https://x.com/yume_arasaki/status/2106837882870886438)
- **GLM-5.3-Flash** `@Morrowmake 配方（TP4，Supermic…` — 4× CMP 170HX 64GB（解锁矿卡） → c=1 结构化 396.0 / 代码 306.2 / 散文 192.5；c=8 798.6 ✅ [来源](https://x.com/seanphan/status/2105673568914898962)
- *……另有 5 条，见 [配方库](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)。*

## 第 4 档 · 14,000–30,000 美元

*3–4 台 Spark 集群、多卡工作站* · 共 8 条


**📝 文字**

- **Qwen3.8-Flash-Next** · Radiance (fork) `Radiance fork · int4fp8 · B…` — 4× AMD R9700 32GB + TR 9970X + 128GB → 48K/用户：538.5 tok/s 合计解码；128K/用户：365 🔁 [来源](https://x.com/richgel999/status/2109515169638326738)
- **Qwen3.8-27B** · Radiance (fork) `MXFP4 · Radiance fork` — 4× R9700（同上 $18k 整机） → 合计解码 900→80 tok/s（4K→128K/会话）；PP 6.3–6.8K 🔁 [来源](https://x.com/richgel999/status/2109515169638326738)
- **GLM-5.3-Flash** `Mia EXL3（TP=3，实验性）` — 3× DGX Spark → 散文 77 单流；4 流 146 🔁 [来源](https://x.com/yume_arasaki/status/2106837882870886438)
- **GLM-5.3-Flash** · TensorFold `TensorFold · Thunderbolt 5×…` — 2× Mac Studio M5 Ultra → 散文 114 单流；PP ~1,600；8 流最高 200；首 token 0.06s 🔁 [来源](https://x.com/yume_arasaki/status/2108359576966094952)
- **DeepSeek-V4.1-Flash** `Mia MXFP4/FP8 · Engram 放 NV…` — 3× DGX Spark → 散文 37.9；4 流合计 78.6（独立 SGLang C1 26.5） 🔁 [来源](https://x.com/yume_arasaki/status/2099966865326170554)
- **DeepSeek-V4.1-Flash** · TensorFold `tonyd615 原生 MXFP4 / Mia Ten…` — 4× DGX Spark → MXFP4：C1 峰值 77.2，6 流 214；TensorFold：散文 87，代码 124.8，4 流 246.8；PP 5,800… 🔁 [来源](https://x.com/yume_arasaki/status/2106837882870886438)
- **DeepSeek-V4.1-Flash** `未注明` — 4× DGX Spark（无交换机直连） → 32 请求时最高 494 tok/s 合计 🔁 [来源](https://x.com/hardfanaticos/status/2107225102475813374)
- **DeepSeek-V4.1-Flash** · MLX `MLX Q4i / DwarfStar` — M3 Ultra 512GB / M5 Max 128GB → ~14.6 / 15（SSD 流式）、25（RDMA 张量并行） 🔁 [来源](https://x.com/yume_arasaki/status/2099966865326170554)

## 价格未公开

按张计价的多卡组合、未标价格的 Mac 以及其他没有单一公开价格的配方 · 共 116 条。按 tok/s 排名靠前的文字配方：

- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2（16GB 配方）` — RTX 5080 16GB → **212 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.6-35B-A3B** · Splash `Splash` — Mac M5 Pro 48GB → **210 tok/s** 🔁 [来源](https://x.com/TeksEdge/status/2101735798567764421)
- **Qwen3.6-35B-A3B** · oMLX `oMLX 0.7.1.dev1 融合解码内核` — Mac M5 Max → **205 tok/s** 🏛️ [来源](https://x.com/jundotkim/status/2108584837590495246)
- **Qwen3.8-Flash-Next-MLX-Serve-iQ-MLX-4.7bpw** · mlx-serve `iQ-MLX 4.7 bpw（校准 4-bit 专家 …` — Mac Studio M5 Ultra → **157 tok/s** 📣 [来源](https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-iQ-MLX-4.7bpw)
- **Qwen3.8-27B** · vLLM `vLLM 等（Reddit u/tonnyygama）` — CMP 170HX（解锁 64GB 矿卡） → **147 tok/s** 🔁 [来源](https://x.com/LFrefman/status/2101572845017178243)
- **Qwen3.8-27B** · Splash `Splash` — Mac M5 Max → **144 tok/s** 🏛️ [来源](https://x.com/zhijianliu/status/2101102949158302001)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2（16GB 配方）` — RTX 5060 Ti 16GB → **128 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **GLM-5.3-Flash** `EXL3（@BrandonMusicKy 权重）+ D…` — 4× DGX Spark + RTX 5090 → **124 tok/s** ✅ [来源](https://x.com/dangerm00se/status/2104876537367728325)
- **Qwen3.8-Flash-Next** · Strata `IQ3_S` — 2× RTX 3090 (48GB) + 64GB DDR5-6000 → **120 tok/s** ✅ [来源](https://x.com/geldeki/status/2109208295957201171) · [指南](recipes/x-004.zh-CN.md)
- **Qwen3.8-Flash-Next** · Strata `q3 xs（Strata 教程）` — 2× Tesla V100 32GB PCIe（无 NVLink） → **120 tok/s** ✅ [来源](https://x.com/rewin123/status/2108669905616736529) · [指南](recipes/x-007.zh-CN.md)
- **Ternary-Bonsai-2-27B-262k** · mirai-s-ada `Ternary Bonsai 2 27B + MTP，…` — RTX 4070 12GB → **102 tok/s** 📣 [来源](https://huggingface.co/CaryPalmer/Ternary-Bonsai-2-27B-262k-GGUF)
- **Qwen3.8-Flash-Next** · Strata `Strata · Q2_0（MTP 投机解码）` — RTX 5070 12GB + Ryzen 5 7600 + 64GB DDR5 → **94 tok/s** 🏛️ [来源](https://github.com/Niko1221/Strata)
- *……全部 116 条见 [配方库](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)。*


## 引擎与工具

| 项目 | ⭐ Star | 实时 | 最后推送 | 简介 |
|---|--:|---|---|---|
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | 131.0k | ![stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat&label=) | 2026-10-13 | 基准 GGUF 引擎，支持 CPU/CUDA/ROCm/Vulkan/Metal。 |
| [vLLM](https://github.com/vllm-project/vllm) | 93.7k | ![stars](https://img.shields.io/github/stars/vllm-project/vllm?style=flat&label=) | 2026-10-13 | 高吞吐推理服务；Spark 上的 MTP 和多路并发配方。 |
| [SGLang](https://github.com/sgl-project/sglang) | 37.1k | ![stars](https://img.shields.io/github/stars/sgl-project/sglang?style=flat&label=) | 2026-10-13 | 推理服务框架；DGX Spark 上与 DFlash2 搭配。 |
| [MLX](https://github.com/ml-explore/mlx) | 28.8k | ![stars](https://img.shields.io/github/stars/ml-explore/mlx?style=flat&label=) | 2026-10-13 | Apple 的数组框架，多数 Mac 配方基于它。 |
| [Strata](https://github.com/Niko1221/Strata) | 23.5k | ![stars](https://img.shields.io/github/stars/Niko1221/Strata?style=flat&label=) | 2026-10-12 | 把 MoE 专家拆到显存、内存和 SSD 的推理引擎，面向 12–24GB 显卡；本库多数 Flash-Next 配方用它。 |
| [oMLX](https://github.com/jundot/omlx) | 22.8k | ![stars](https://img.shields.io/github/stars/jundot/omlx?style=flat&label=) | 2026-10-13 | Apple Silicon 上的 MLX 推理服务，支持连续批处理和分层 KV/SSD 缓存。 |
| [DFlash / DFlash 2](https://github.com/z-lab/dflash) | 6.2k | ![stars](https://img.shields.io/github/stars/z-lab/dflash?style=flat&label=) | 2026-08-18 | 块扩散投机解码；DFlash 2 提供 Qwen3.8-27B 草稿模型。 |
| [LightX2V](https://github.com/ModelTC/LightX2V) | 2.9k | ![stars](https://img.shields.io/github/stars/ModelTC/LightX2V?style=flat&label=) | 2026-10-13 | 视频生成推理框架，有 5090 上的 MiniMax H3 结果。 |
| [TensorFold](https://github.com/ashhart/TensorFold) | 1.3k | ![stars](https://img.shields.io/github/stars/ashhart/TensorFold?style=flat&label=) | 2026-10-12 | 兼容 OpenAI 接口的 MoE 运行时，带投机解码；也用于 ComfyUI 里的 MiniMax H3。 |
| [halogen](https://github.com/peonist-ai/halogen-flash-server) | 954 | ![stars](https://img.shields.io/github/stars/peonist-ai/halogen-flash-server?style=flat&label=) | 2026-10-13 | 针对 Strix Halo 调优的 Flash-Next 服务。 |
| [dflash-mlx](https://github.com/bstnxbt/dflash-mlx) | 788 | ![stars](https://img.shields.io/github/stars/bstnxbt/dflash-mlx?style=flat&label=) | 2026-08-20 | Apple Silicon（MLX）上的 DFlash 投机解码。 |
| [FastH3](https://haoailab.com/blogs/fasth3-rtx/) | — | *（网站/博客）* | — | Hao AI Lab 的 8 步蒸馏版 MiniMax H3，面向 RTX 显卡（博客）。 |

<sub>⭐ 快照由 `scripts/update_stars.py` 更新于 2026-10-13T14:44Z（UTC）· 「实时」徽章由 shields.io 在打开页面时实时渲染。</sub>

## 相关榜单与清单

| 项目 | ⭐ Star | 实时 | 最后推送 | 简介 |
|---|--:|---|---|---|
| [Awesome-LLM-Inference](https://github.com/xlite-dev/Awesome-LLM-Inference) | 5.5k | ![stars](https://img.shields.io/github/stars/xlite-dev/Awesome-LLM-Inference?style=flat&label=) | 2026-08-14 | 推理方向论文与代码合集。 |
| [awesome-local-llm](https://github.com/rafska/awesome-local-llm) | 3.0k | ![stars](https://img.shields.io/github/stars/rafska/awesome-local-llm?style=flat&label=) | 2026-10-12 | 本地大模型平台与工具目录。 |
| [LocalScore](https://github.com/cjpais/LocalScore) | 134 | ![stars](https://img.shields.io/github/stars/cjpais/LocalScore?style=flat&label=) | 2026-10-09 | 标准化的单卡跑分 CLI。 |
| [llamabench.ai](https://llamabench.ai/) | — | *（网站/博客）* | — | llama.cpp 跑分结果，附完整启动命令。 |
| [llamaperf](https://llamaperf.com/leaderboard) | — | *（网站/博客）* | — | 社区自报排行榜（给中位数）。 |
| [canirun.ai](https://canirun.ai/) | — | *（网站/博客）* | — | 估算模型能否在你的硬件上运行、跑多快。 |

<sub>⭐ 快照由 `scripts/update_stars.py` 更新于 2026-10-13T14:44Z（UTC）· 「实时」徽章由 shields.io 在打开页面时实时渲染。</sub>

## 参与贡献

一条配方一个 PR。从 [提交页](https://raytone-lab.github.io/Awesome-local-inference-recipe/submit.html) 复制 YAML 模板，只填来源里写明的内容（其余写 `null`），运行 `node scripts/validate.mjs` 校验并附上原帖链接。然后运行 `python3 scripts/gen_readme.py` 重新生成两份 README。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

本地开发：`python3 -m http.server 5190` → `index.html`（首页）· `explore.html`（筛选、排序、散点图）· 数据格式见 [`schema/recipe.schema.json`](schema/recipe.schema.json)。

<details><summary>网站预览</summary>

<img src="docs/screenshot.png" width="760" alt="RecipeBench">

</details>

## 许可证

- 代码：[MIT](LICENSE)
- 数据（`data/`）：[CC BY 4.0](LICENSE-DATA)。可自由使用，需署名 RecipeBench 并保留每条配方的原始来源链接。
