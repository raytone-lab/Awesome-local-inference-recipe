# Awesome Local Inference Recipes [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Model × engine × hardware → measured speed and cost, with every number linked to its source. Consumer and used hardware, ≤ $30k.
> 本地推理配方：跨引擎、消费级/二手硬件、每个数字标来源。

<sub>Working name: **RecipeBench** (placeholder) · 176 recipes (135 text · 16 image · 25 video/audio) · data as of 2026-10-13 · <a href="explore.html">Explorer</a> · <a href="submit.html">Submit</a></sub>

## Contents

- [Legend](#legend)
- [Hot This Month](#hot-this-month)
- [Tier 1 · ≤ $2.5k](#tier-1---25k)
- [Tier 2 · $2.5k–7k](#tier-2--25k7k)
- [Tier 3 · $7k–14k](#tier-3--7k14k)
- [Tier 4 · $14k–30k](#tier-4--14k30k)
- [Cost Not Published](#cost-not-published)
- [Engines & Tools](#engines--tools)
- [Related Lists & Benchmarks](#related-lists--benchmarks)
- [Contributing](#contributing)
- [License](#license)

## Legend

| Source level | | Format |
|---|---|---|
| 🏛️ **官方** Official | vendor/project number | `Model · Engine` `quant` — Hardware → **key number** level [source] |
| ✅ **实测** Measured | author ran it, log/screenshot | **tok/s** = single-stream generation (not prefill, not aggregate) |
| 🔁 **转述** Relayed | second-hand, verify upstream | Tiers use the lowest published hardware price (USD) |
| 📣 **宣称** Claimed | projection, no repro | Unknown fields are never estimated (未见公开数据) |

## Hot This Month

Most-engaged recipe posts on X, 2026-09-15 → 10-13 (likes + 3×reposts).

- **MiniMax H3** · ComfyUI — 笔记本 RTX 5090 24GB + 64GB RAM → 3 段 5s 衔接片段共 17 分钟 ✅ [@EndFolding79421](https://x.com/EndFolding79421/status/2102448683245502844) ♥149
- **GLM 5.3（帖文原话 “GLM 5.3 Code”）** · oMLX（作者调优） — Mac Studio M5 Ultra → **87 tok/s** ✅ [@JamesMcPherson](https://x.com/JamesMcPherson/status/2104028051285672431) ♥106
- **Qwen3.8-Flash-Next** · Strata — AMD Strix Halo 395 → **47.7 tok/s** ✅ [@no_stp_on_snek](https://x.com/no_stp_on_snek/status/2108296174994088177) ♥73
- **Qwen3.8-Flash-Next** · Strata — 笔记本 RTX 5070 Ti 12GB + Intel 275HX + 64GB DDR5 + … → **51 tok/s** 🔁 [@jurlycat](https://x.com/jurlycat/status/2105165498967007621) ♥46
- **Qwen3.8-Flash-Next** · Strata v0.1.42 — 2× RTX 3090 (48GB) + 64GB DDR5-6000 → **120 tok/s** ✅ [@geldeki](https://x.com/geldeki/status/2109208295957201171) ♥45
- **Qwen3.8-Flash-Next** · 其他/未注明 — Mac Studio M5 Ultra → **85.9 tok/s** 🔁 [@wei_wang](https://x.com/wei_wang/status/2103459506944344323) ♥33
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s 视频+音频 ≈72 s（稳态，不含 MP4 导出；基线 ~26 分钟） 🏛️ [@LightX2V](https://x.com/LightX2V/status/2108769912009424976) ♥8
- **MiniMax H3** · TensorFold（ComfyUI 换 loader） — RTX 5070 Ti 16GB + 64GB RAM（Windows） → 1344×768 5s 带声音：81 s（原生 ComfyUI 20 步 623 s） ✅ [@jayleaton](https://x.com/jayleaton/status/2106213885917491367) ♥10

## Tier 1 · ≤ $2.5k

*Used 3090/4090, MI50/V100 cards, Strix Halo, R9700* · 31 recipes


**📝 Text**

- **Qwen3.8-Flash-Next** · Strata `Strata（作者自改版）· Swift 1.5 IQ…` — RTX 4090 24GB + 32GB DDR5 → **220 tok/s** ✅ [source](https://x.com/Knuckles_XBT/status/2105245662657011841)
- **Qwen3.6-35B-A3B** `FreeToken · NVFP4（无投机）` — RTX 4090 → **167 tok/s** 🔁 [source](https://x.com/shipfrontierai/status/2092602493213577481)
- **Qwen3.8-27B** · DFlash `DFlash2（TeksEdge）` — RTX 3090 24GB → **138 tok/s** 🔁 [source](https://x.com/yume_arasaki/status/2090971775714939097)
- **Qwen3.8-27B** · DFlash `EXL3 4.0bpw + DFlash2 草稿（r0…` — RTX 4090 24GB → **121 tok/s** ✅ [source](https://x.com/yume_arasaki/status/2100595901006008791)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S（GSQ-RCO）` — 单 RTX 3090 24GB（+64GB RAM 同作者前帖） → **120.8 tok/s** ✅ [source](https://x.com/needmorevram/status/2105050786938118599)
- **Qwen3.8-Flash-Next** · Strata（PR #262） `Q2_0` — AMD Radeon AI PRO R9700 → **100 tok/s** ✅ [source](https://x.com/TechPractice1/status/2105338176055509376)
- **Qwen3.8-27B** · llama.cpp `llama.cpp + MTP（Vulkan，Wind…` — AMD RX 7900 XTX → **85.4 tok/s** ✅ [source](https://x.com/sudoingX/status/2094673741125140658)
- **Qwen3.8-Flash-Next** · Strata `GSQ-RCO IQ3_XXS` — RTX 4090 24GB + RAM（专家 39.97GiB 放内存） → **78.6 tok/s** ✅ [source](https://x.com/BrianMRey/status/2103789711311413320)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S（GSQ-RCO）` — RTX 3090 24GB → **72 tok/s** ✅ [source](https://x.com/needmorevram/status/2104898095318544540)
- **Qwen3.8-Flash-Next** · llama.cpp `llama.cpp PR #29887 MoE 专家 …` — RTX 4090 / RTX 5090 + 系统内存 → **68 tok/s** 🏛️ [source](https://github.com/ggml-org/llama.cpp/pull/29887)
- *…and 13 more in the [explorer](explore.html).*

**🖼️ Image**

- **Qwen-Image 2.1（7B + 8B 文本编码器）** · ComfyUI `官方 Comfy-Org INT8 · ComfyUI` — RTX 4090 24GB → 8.1 s / 1024²（40 步）；30.2 s / 2048×1152（50 步）；峰值 16.2GB ✅ [source](https://x.com/yume_arasaki/status/2102176739359404499)
- **Qwen-Image 2.1** `INT8` — RTX 3090 → 82–96 s / 2K（公开回执） 🔁 [source](https://x.com/yume_arasaki/status/2102176739359404499)
- **Qwen-Image 2.1（编辑）** · ComfyUI `ComfyUI` — Mac M4 Pro → 3 分 52 秒 / 张（768 编辑） ✅ [source](https://x.com/gabeciii/status/2104920039077884324)
- **Z-Image Turbo（6B，8 步）** · ComfyUI `ComfyUI` — RTX 3090 24GB → 2048px 约 8 s / 张；另一用户预热后 12 s ✅ [source](https://x.com/michaelricks/status/2104959036353356058)

**🎬 Video & Audio**

- **FastH3 V2 / Trim** `FP8` — RTX 4090 24GB → 480p 5s：54.6 / 43.9 s；768p：154.6 / 132.8 s；8GB 限制 Trim 82.0 s 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3（turbo）** · ComfyUI `ComfyUI` — RTX 4090 → 5 s 片段 ~91 s；15 s ~8 分钟；960×544×5s 约 50 s ✅ [source](https://x.com/yume_arasaki/status/2097790831323427046)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 3090 → 11 s 视频 13 分钟 ✅ [source](https://x.com/natehalko/status/2103538997146611890)
- **ACE-Step 1.5（音乐）** — RTX 3090 → 整首歌 <10 s（宣传帖） 🔁 [source](https://x.com/simplifyinAI/status/2091935190335754493)

## Tier 2 · $2.5k–7k

*One RTX 5090, one DGX Spark, Mac Studio Max* · 61 recipes


**📝 Text**

- **Qwen3.6-35B-A3B** `sparkinfer v0.4.4（Blackwell…` — RTX 5090 → **512 tok/s** 📣 [source](https://x.com/kysstalol/status/2105042922643321008)
- **Qwen3.6-35B-A3B** · DFlash `DFlash 2` — Mac Studio M3 Ultra → **251 tok/s** ✅ [source](https://x.com/tinybluedev/status/2089910202606764530)
- **Qwen3.8-Flash-Next** · Strata v0.1.27 `IQ2_XS` — RTX 5090 + 256GB RAM → **176 tok/s** ✅ [source](https://x.com/TechPractice1/status/2105087037363884483)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090（RAM 未注明） → **160 tok/s** 🔁 [source](https://x.com/yume_arasaki/status/2107293459556225446)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090（功耗限制）+ 96GB DDR5-6400 → **150 tok/s** 🔁 [source](https://x.com/kreia/status/2106054715373212025)
- **Qwen3.8-Flash-Next** · TensorFold `TensorFold 0.3.4.x + PR 29/…` — Mac Studio M3 Ultra → **130 tok/s** ✅ [source](https://x.com/ivanfioravanti/status/2104183112611614780)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090 → **123.4 tok/s** ✅ [source](https://x.com/needmorevram/status/2104995992273871104)
- **Qwen3.8-27B** · TensorFold — DGX Spark → **102.9 tok/s** 🔁 [source](https://x.com/HandwerkAiLab/status/2104169723684679799)
- **Qwen3.8-Flash-Next** · oMLX `4-bit MTP（oMLX PR / OMP）` — Mac Studio M3 Ultra → **97.1 tok/s** ✅ [source](https://x.com/Oluwaphilemon1/status/2099312823025496405)
- **Qwen3.8-Flash-Next** · ExLlama `Cruz exllamav3 fork · EXL3 …` — 1× DGX Spark → **71.7 tok/s** ✅ [source](https://x.com/yume_arasaki/status/2101741448811229219)
- *…and 33 more in the [explorer](explore.html).*

**🖼️ Image**

- **Qwen-Image 2.1** `LightX2V / BennyDaBall NVFP…` — RTX 5090 32GB → 5.93 s；NVFP4 6.7 s vs INT8 7.6 s vs BF16 15.6 s（1024²） 🔁 [source](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image 2.1** · TensorFold `TensorFold NVFP4 / FP8 / GG…` — RTX 5090 @450W → 4.53 s / 6.94 s / 13.87 s（1024²，25 步；NVFP4 峰值 22.9GB；图像与 Q6 不完全一致） ✅ [source](https://x.com/niklaslenz_ai/status/2106465941177487871)
- **Qwen-Image 2.1** `厂商内核重写+步缓存` — RTX 5090 → 13.5 s → 1.9 s / 张（厂商宣称） 📣 [source](https://x.com/fractalyze_io/status/2105207217452695841)
- **Qwen-Image 2.1** · SGLang `spark-image-lab BF16 / SGLa…` — 1× DGX Spark（对照 4090） → 52.6 s / 1024²；SGLang 表：Spark 35.4 s，4090 18.7 s 🔁 [source](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image-2.1-Turbo（官方 8 步）** `Turbo 8 步 vs Base 40 步` — RTX 5090 → 29 s vs 108 s / 张（2048²） ✅ [source](https://x.com/niklaslenz_ai/status/2108609693941920176)
- **Z-Image Turbo vs Qwen-Image 2.1** `同 prompt 同 seed 20 轮` — RTX 5090 → Z-Image 快约 2×（无绝对时间）；质量 Qwen 9:6 胜 ✅ [source](https://x.com/princedoesai/status/2109376490009743713)

**🎬 Video & Audio**

- **FastH3 V2（MiniMax H3 8 步蒸馏）** `NVFP4` — RTX 5090 32GB → 832×480×5s：14.8 s；1344×768×5s：38.6 s（含音频，端到端） 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/)
- **FastH3 Trim（42 块剪枝，实验）** `NVFP4` — RTX 5090 → 480p 5s：13.4 s；768p：35.4 s 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/)
- **FastH3 V2 / Trim** `NVFP4` — 1× / 2× DGX Spark → 1×：480p 141.4 / 125.8 s，Trim 768p 340.1 s；2×：87.2 / 78.3 s 🏛️ [source](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3（基础，50 步类）** · ComfyUI `ComfyUI + SageAttention` — RTX 5090 → 1280×736×5s：242 s → 168 s ✅ [source](https://x.com/RKAScope/status/2084359480926503182)
- **MiniMax H3 vs FastH3 Turbo** `同图同 seed` — RTX 5090 → 15 s 片段：11 分 55 秒 vs 2 分 6 秒 ✅ [source](https://x.com/Sogni_Protocol/status/2097254959729246550)
- **MiniMax H3（Sol 加速 / 无加速）** `NVIDIA Sol 引擎` — 1× DGX Spark → Sol：480p 5 s 约 68 s（NVIDIA 公布 56 s）；无 Sol >400 s；无 Sol 720p 20 步：5 s … ✅ [source](https://x.com/yume_arasaki/status/2100734364908986511)
- **MiniMax H3 vs LTX-2.3 Eros** `同条件 3 组 prompt` — 1× DGX Spark → 864×480×5s：H3 平均 270 s；LTX 154 s（快 1.76×） ✅ [source](https://x.com/YRSM_Simon/status/2084222856972456336)
- **LTX-2.3（带口型同步）** · ComfyUI `ComfyUI` — RTX 5090 → 10 s 约 90 s（较弱 GPU 约 6×） ✅ [source](https://x.com/freshstartsnow/status/2092263835591655773)
- **LTX-2.5（t2v）** `模板 + LoRA` — RTX 5090（500W） → 720p/10 s：61.11 s；1080p/10 s：189.90 s ✅ [source](https://x.com/PhotogenicWeekE/status/2087298681137701274)
- **ACE-Step 1.5 + LTX-2.3** · ComfyUI `ComfyUI 串行工作流` — 1× DGX Spark → 2 分 05 秒歌曲一次生成；+2:28 口型视频端到端 32 分钟 🔁 [source](https://x.com/yume_arasaki/status/2100734364908986511)
- **Wan2.1 14B（SparkDiffusion）** `97% 稀疏注意力 + 3 步蒸馏 + FP8` — RTX 5090 → 720p：4,769 s → 18 s（项目宣称 265×） 📣 [source](https://x.com/thePandaily/status/2105209996648567243)
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s 视频+音频 ≈72 s（稳态，不含 MP4 导出；基线 ~26 分钟） 🏛️ [source](https://x.com/LightX2V/status/2108769912009424976)

## Tier 3 · $7k–14k

*Two Sparks, Mac Studio Ultra* · 15 recipes


**📝 Text**

- **Qwen3.8-Flash-Next** · TensorFold `TensorFold · NVFP4 全模型 / IN…` — 2× DGX Spark → **67.4 tok/s** 🔁 [source](https://x.com/llm_frontier_jp/status/2108884169069916440)
- **GLM-5.3-Flash** · TensorFold 0.5.0 + DFlash2 草稿 — 2× DGX Spark（TP2） → **54 tok/s** ✅ [source](https://x.com/easthambuilds/status/2105693180427452703)
- **DeepSeek-V4.1-Flash** `Mia EXL3 2.9bpw · DSpark k=…` — 2× DGX Spark → **48.5 tok/s** ✅ [source](https://x.com/yume_arasaki/status/2099966865326170554)
- **GLM-5.3-Flash** `未注明` — 2× DGX Spark → **30 tok/s** ✅ [source](https://x.com/realWeZZard/status/2099322375770869891)
- **Qwen3.8-Flash-Next** · vLLM `vr8vr8 v4.1 配方（vLLM，TP=2）` — 2× DGX Spark → 散文 81.6；结构化 138.3；代码 133.2；4 流结构化合计 383.1 ✅ [source](https://x.com/yume_arasaki/status/2104582876956332408)
- **Qwen3.8-Flash-Next** · oMLX `fused-kernel oMLX 分支` — Mac Studio M3 Ultra 256GB → 102 单流；8 流 134（stock oMLX 25） 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- **Qwen3.8-Flash-Next** · oMLX `调优 oMLX / TensorFold` — Mac Studio M5 Ultra 80C 256GB → oMLX 157.7（195K 时 96.6）；TensorFold 200.7 解码但仅 471 PP（oMLX 3,300–3,600） 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- **Qwen3.8-27B** · TensorFold `TensorFold 1.0.7（采样模式也可起草）` — Mac Studio M3 Ultra → 代码 125；散文 51（1.0.5 约 20） 🏛️ [source](https://x.com/VRAMCalculator/status/2109344267994808619)
- **GLM-5.3-Flash** · TensorFold `Mia EXL3 + TensorFold（TP=2）` — 2× DGX Spark → 散文 60.4；结构化 114.7；4 流合计 108.8；8K 54.9 → 874K 44.6 ✅ [source](https://x.com/yume_arasaki/status/2106837882870886438)
- **GLM-5.3-Flash** `@Morrowmake 配方（TP4，Supermic…` — 4× CMP 170HX 64GB（解锁矿卡） → c=1 结构化 396.0 / 代码 306.2 / 散文 192.5；c=8 798.6 ✅ [source](https://x.com/seanphan/status/2105673568914898962)
- *…and 5 more in the [explorer](explore.html).*

## Tier 4 · $14k–30k

*3–4 Spark clusters, multi-GPU workstations* · 8 recipes


**📝 Text**

- **Qwen3.8-Flash-Next** `Radiance fork · int4fp8 · B…` — 4× AMD R9700 32GB + TR 9970X + 128GB → 48K/用户：538.5 tok/s 合计解码；128K/用户：365 🔁 [source](https://x.com/richgel999/status/2109515169638326738)
- **Qwen3.8-27B** `MXFP4 · Radiance fork` — 4× R9700（同上 $18k 整机） → 合计解码 900→80 tok/s（4K→128K/会话）；PP 6.3–6.8K 🔁 [source](https://x.com/richgel999/status/2109515169638326738)
- **GLM-5.3-Flash** `Mia EXL3（TP=3，实验性）` — 3× DGX Spark → 散文 77 单流；4 流 146 🔁 [source](https://x.com/yume_arasaki/status/2106837882870886438)
- **GLM-5.3-Flash** · TensorFold `TensorFold · Thunderbolt 5×…` — 2× Mac Studio M5 Ultra → 散文 114 单流；PP ~1,600；8 流最高 200；首 token 0.06s 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- **DeepSeek-V4.1-Flash** `Mia MXFP4/FP8 · Engram 放 NV…` — 3× DGX Spark → 散文 37.9；4 流合计 78.6（独立 SGLang C1 26.5） 🔁 [source](https://x.com/yume_arasaki/status/2099966865326170554)
- **DeepSeek-V4.1-Flash** · TensorFold `tonyd615 原生 MXFP4 / Mia Ten…` — 4× DGX Spark → MXFP4：C1 峰值 77.2，6 流 214；TensorFold：散文 87，代码 124.8，4 流 246.8；PP 5,800… 🔁 [source](https://x.com/yume_arasaki/status/2106837882870886438)
- **DeepSeek-V4.1-Flash** `未注明` — 4× DGX Spark（无交换机直连） → 32 请求时最高 494 tok/s 合计 🔁 [source](https://x.com/hardfanaticos/status/2107225102475813374)
- **DeepSeek-V4.1-Flash** · MLX `MLX Q4i / DwarfStar` — M3 Ultra 512GB / M5 Max 128GB → ~14.6 / 15（SSD 流式）、25（RDMA 张量并行） 🔁 [source](https://x.com/yume_arasaki/status/2099966865326170554)

## Cost Not Published

*Multi-card builds priced per card, Macs without a listed price, and other rows with no single published price* · 61 recipes. Top text recipes by tok/s:

- **Qwen3.6-35B-A3B** `Splash` — Mac M5 Pro 48GB → **210 tok/s** 🔁 [source](https://x.com/TeksEdge/status/2101735798567764421)
- **Qwen3.6-35B-A3B** · oMLX `oMLX 0.7.1.dev1 融合解码内核` — Mac M5 Max → **205 tok/s** 🏛️ [source](https://x.com/jundotkim/status/2108584837590495246)
- **Qwen3.8-27B** · vLLM `vLLM 等（Reddit u/tonnyygama）` — CMP 170HX（解锁 64GB 矿卡） → **147 tok/s** 🔁 [source](https://x.com/LFrefman/status/2101572845017178243)
- **Qwen3.8-27B** `Splash` — Mac M5 Max → **144 tok/s** 🏛️ [source](https://x.com/zhijianliu/status/2101102949158302001)
- **GLM-5.3-Flash** `EXL3（@BrandonMusicKy 权重）+ D…` — 4× DGX Spark + RTX 5090 → **124 tok/s** ✅ [source](https://x.com/dangerm00se/status/2104876537367728325)
- **Qwen3.8-Flash-Next** · Strata v0.1.42 `IQ3_S` — 2× RTX 3090 (48GB) + 64GB DDR5-6000 → **120 tok/s** ✅ [source](https://x.com/geldeki/status/2109208295957201171)
- **Qwen3.8-Flash-Next** · Strata `q3 xs（Strata 教程）` — 2× Tesla V100 32GB PCIe（无 NVLink） → **120 tok/s** ✅ [source](https://x.com/rewin123/status/2108669905616736529)
- **Qwen3.8-Flash-Next** · Strata `Strata · Q2_0（MTP 投机解码）` — RTX 5070 12GB + Ryzen 5 7600 + 64GB DDR5 → **94 tok/s** 🏛️ [source](https://github.com/Niko1221/Strata)
- **Qwen3.8-Flash-Next** · MLX `mlx-serve · Sushi-4 混合精度包` — Mac M5 Max 128GB → **90 tok/s** 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- **GLM 5.3（帖文原话 “GLM 5.3 Code”）** · oMLX（作者调优） — Mac Studio M5 Ultra → **87 tok/s** ✅ [source](https://x.com/JamesMcPherson/status/2104028051285672431)
- **Qwen3.8-Flash-Next** — Mac Studio M5 Ultra → **85.9 tok/s** 🔁 [source](https://x.com/wei_wang/status/2103459506944344323)
- **Qwen3.8-Flash-Next** · oMLX `oMLX 0.6.4 · MTP depth 6` — Mac M4 Max 128GB → **83 tok/s** 🔁 [source](https://x.com/yume_arasaki/status/2108359576966094952)
- *…browse all 61 in the [explorer](explore.html).*


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
