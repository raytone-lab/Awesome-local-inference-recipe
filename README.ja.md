<h1 align="center">ローカル推論レシピ集 <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a></h1>

<p align="center">あなたのハードウェアで、実際どれくらいの速度が出る？出典付きのローカル AI レシピ 288 件。405 ドルの GPU から 3 万ドルの構成まで。</p>

<p align="center"><a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <b>日本語</b></p>

<p align="center"><a href="https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html"><img src="https://img.shields.io/badge/recipes-288-0891B2?style=flat-square" alt="288 recipes"></a> <img src="https://img.shields.io/badge/data%20as%20of-2026--10--13-4B5563?style=flat-square" alt="data as of 2026-10-13"> <a href="https://github.com/raytone-lab/Awesome-local-inference-recipe/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/raytone-lab/Awesome-local-inference-recipe/validate.yml?branch=main&style=flat-square&label=validate" alt="validate"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-22C55E?style=flat-square" alt="MIT"></a> <a href="LICENSE-DATA"><img src="https://img.shields.io/badge/data-CC%20BY%204.0-22C55E?style=flat-square" alt="CC BY 4.0"></a> <a href="https://github.com/raytone-lab/Awesome-local-inference-recipe/stargazers"><img src="https://img.shields.io/github/stars/raytone-lab/Awesome-local-inference-recipe?style=flat-square" alt="GitHub stars"></a> <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-7C3AED?style=flat-square" alt="PRs welcome"></a></p>

<p align="center"><a href="https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html"><b>エクスプローラー</b></a> · <a href="recipes/README.ja.md"><b>レシピガイド</b></a> · <a href="docs/getting-started.ja.md"><b>はじめに</b></a> · <a href="https://raytone-lab.github.io/Awesome-local-inference-recipe/submit.html"><b>レシピを投稿</b></a></p>

<p align="center"><img src="docs/hero.ja.png" width="860" alt="棒グラフ：ハードウェア $1,000 あたりの tok/s で並べた実測テキスト構成トップ 15（ハードウェア分類で色分け）"></p>

**レシピ 288 件**（テキスト 247 · 画像 16 · 動画・音声 25）· **ハードウェア 6 分類** · **エンジン 34 種** · **モデルファミリー 11 系統** · すべての数字に出典リンク · 予算 **3 万ドルまで**

### 注目の記録

| 記録               | モデル · エンジン                   | ハードウェア                                                | 結果               | 出典                                                                       |
| ---------------- | ---------------------------- | ----------------------------------------------------- | ---------------- | ------------------------------------------------------------------------ |
| Mac で最速          | Qwen3.6-35B-A3B · DFlash     | Mac Studio M3 Ultra · 約 5,649 ドル（最小構成価格、検証機のメモリは不明）   | **251 tok/s** ✅  | [出典](https://x.com/tinybluedev/status/2089910202606764530)               |
| RTX 5090 1 枚で最速  | Qwen3.8-Flash-Next · Strata  | RTX 5090 + 256GB RAM · 約 5,400 ドル（GPU のみ、256GB RAM 別） | **176 tok/s** ✅  | [@TechPractice1](https://x.com/TechPractice1/status/2105087037363884483) |
| AMD で最速          | Qwen3.8-Flash-Next · Strata  | AMD Radeon AI PRO R9700 · 約 1,600 ドル                  | **100 tok/s** ✅  | [@TechPractice1](https://x.com/TechPractice1/status/2105338176055509376) |
| 中古データセンター GPU    | Qwen3.8-Flash-Next · Strata  | 2× Tesla V100 32GB PCIe                               | **120 tok/s** ✅  | [@rewin123](https://x.com/rewin123/status/2108669905616736529)           |
| DGX Spark 1 台で最速 | Qwen3.8-Flash-Next · ExLlama | 1× DGX Spark · 約 6,950 ドル                             | **71.7 tok/s** ✅ | [出典](https://x.com/yume_arasaki/status/2101741448811229219)              |
| いちばん安い構成         | Qwen3.8-Flash-Next · Strata  | Tesla P40 24GB · 約 405 ドル                             | **30 tok/s** ✅   | [出典](https://github.com/Niko1221/Strata/blob/main/docs/OLDER_GPUS.md)    |

<sub>1 ストリームの生成速度で、いずれも出典からの引用です。価格は公開されている最安のハードウェア価格。✅ = 投稿者本人の実測。</sub>

## 目次

- [凡例](#凡例)
- [今月の注目](#今月の注目)
- [モデルファミリー別](#モデルファミリー別)
- [エンジン別](#エンジン別)
- [第 1 段階 · 2,500 ドルまで](#第-1-段階--2500-ドルまで)
- [第 2 段階 · 2,500〜7,000 ドル](#第-2-段階--25007000-ドル)
- [第 3 段階 · 7,000〜14,000 ドル](#第-3-段階--700014000-ドル)
- [第 4 段階 · 14,000〜30,000 ドル](#第-4-段階--1400030000-ドル)
- [価格非公開](#価格非公開)
- [エンジンとツール](#エンジンとツール)
- [関連リスト・ベンチマーク](#関連リストベンチマーク)
- [ライセンス](#ライセンス)

## 凡例

| 出典レベル      | 意味                       | 表記                                                   |
| ---------- | ------------------------ | ---------------------------------------------------- |
| 🏛️ **公式** | 開発元やベンダーが公表した数字          | **モデル** · エンジン `量子化` — ハードウェア → **主要な数字** レベル \[出典\] |
| ✅ **実測**   | 投稿者本人が計測（ログやスクリーンショットあり） | **tok/s** は 1 ストリームの生成速度（プリフィルや合計値は含まない）             |
| 🔁 **伝聞**  | 他人の結果の引用。元の投稿で確認を        | 価格帯は公開されている最安のハードウェア価格（米ドル）で区分                       |
| 📣 **主張**  | 見込み値で、再現条件なし             | 不明な値は推定しません                                          |

## 今月の注目

2026-09-15〜10-13 に X で反応が多かったレシピ投稿（いいね + リポスト×3 の順）。

- **DeepSeek-V4.1-Flash** — 2× DGX Spark → **29 tok/s** ✅ [@0xSero](https://x.com/0xSero/status/2106373861818224907) ♥2470
- **Qwen3.8-Flash-Next** · vLLM — 1× DGX Spark → **48.7 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2101339268203380857) ♥800
- **GLM-5.3-Flash EXL3 4-bit** · TensorFold — 2× DGX Spark → **60.4 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2105598458547646875) ♥683
- **Qwen3.8-Flash-Next** — RTX 3090 24GB + 64GB DDR4/5 + 100GB NVMe → **64 tok/s** 📣 [@0xSero](https://x.com/0xSero/status/2104865431659892934) ♥686
- **Qwen3.8-Flash-Next** · TensorFold — 1× DGX Spark → **64.4 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2108203605685596490) ♥386
- **DeepSeek-V4-Flash (0731 GA)** — 2× DGX Spark → **82 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2083326111144906836) ♥368
- **Qwen3.8-27B** · vLLM — RTX 5090 32GB → **147 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2088734058842878037) ♥381
- **Qwen3.6-35B-A3B** · vLLM — 1× DGX Spark → **95 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2082573590529204458) ♥311

## モデルファミリー別

ファミリー名をクリックすると、絞り込み済みのエクスプローラーが開きます。タグ：[`dense`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=dense) 97, [`long-context`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=long-context) 94, [`speculative`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=speculative) 81, [`4bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=4bit) 73, [`MTP`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=MTP) 52, [`multi-GPU`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=multi-GPU) 40, [`MoE`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=MoE) 35, [`3bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=3bit) 32, [`2bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=2bit) 24, [`8bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=8bit) 23, [`ternary`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=ternary) 22, [`1bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=1bit) 12, [`few-step`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=few-step) 12, [`offload`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=offload) 11, [`bf16`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=bf16) 6, [`6bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=6bit) 6, [`abliterated`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=abliterated) 2, [`5bit`](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?tag=5bit) 1。

| ファミリー                                                                                                       | レシピ数 | テキスト | 画像  | 動画・音声 |
| ----------------------------------------------------------------------------------------------------------- | ---- | ---- | --- | ----- |
| [Qwen](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Qwen)               | 162  | 162  |     |       |
| [Bonsai](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Bonsai)           | 29   | 29   |     |       |
| [GLM](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=GLM)                 | 23   | 23   |     |       |
| [DeepSeek](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=DeepSeek)       | 22   | 22   |     |       |
| [MiniMax H3](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=MiniMax%20H3) | 17   |      |     | 17    |
| [Qwen-Image](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Qwen-Image)   | 13   |      | 13  |       |
| [LTX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=LTX)                 | 4    |      |     | 4     |
| [Z-Image](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Z-Image)         | 3    |      | 3   |       |
| [ACE-Step](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=ACE-Step)       | 2    |      |     | 2     |
| [Edge0](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Edge0)             | 2    | 2    |     |       |
| [Wan](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Wan)                 | 2    |      |     | 2     |
| [Other](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?family=Other)             | 9    | 9    |     |       |

## エンジン別

エンジン名は表記を統一しています（`scripts/normalize_engines.py`）。元の表記は `engine_note` に残しています。

| エンジン                                                                                                                                                | レシピ数 |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| [oMLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=oMLX)                                                       | 30   |
| [Strata](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Strata)                                                   | 29   |
| [llama.cpp](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp)                                             | 28   |
| [TensorFold](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=TensorFold)                                           | 21   |
| [MLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX)                                                         | 17   |
| [llama.cpp (PrismML fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28PrismML%20fork%29)       | 14   |
| [ComfyUI](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ComfyUI)                                                 | 12   |
| [MTPLX](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MTPLX)                                                     | 11   |
| [SGLang](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=SGLang)                                                   | 9    |
| [vLLM](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=vLLM)                                                       | 9    |
| [DFlash](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=DFlash)                                                   | 7    |
| [mlx-serve](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mlx-serve)                                             | 7    |
| [Splash](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Splash)                                                   | 5    |
| [Project Maya](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Project%20Maya)                                     | 4    |
| [mirai-s-ada](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mirai-s-ada)                                         | 4    |
| [ds4 (DwarfStar)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ds4%20%28DwarfStar%29)                           | 3    |
| [llama.cpp (agentionai fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28agentionai%20fork%29) | 3    |
| [Halogen](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Halogen)                                                 | 2    |
| [MLX Swift](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX%20Swift)                                           | 2    |
| [Ollama](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Ollama)                                                   | 2    |
| [Radiance (fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Radiance%20%28fork%29)                           | 2    |
| [edge0](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=edge0)                                                     | 2    |
| [DS41RT](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=DS41RT)                                                   | 1    |
| [ExLlama](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=ExLlama)                                                 | 1    |
| [FreeToken](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=FreeToken)                                             | 1    |
| [LightX2V](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=LightX2V)                                               | 1    |
| [MLX Swift (PrismML fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=MLX%20Swift%20%28PrismML%20fork%29)     | 1    |
| [NVIDIA Sol](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=NVIDIA%20Sol)                                         | 1    |
| [Osaurus](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Osaurus)                                                 | 1    |
| [TabbyAPI](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=TabbyAPI)                                               | 1    |
| [llama.cpp (mirai-s fork)](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=llama.cpp%20%28mirai-s%20fork%29)       | 1    |
| [mflux](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=mflux)                                                     | 1    |
| [sparkinfer](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=sparkinfer)                                           | 1    |
| [sushi](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=sushi)                                                     | 1    |
| [Unspecified](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html?engine=Unspecified)                                         | 53   |

<p align="center"><img src="docs/budget-tiers.ja.png" width="860" alt="棒グラフ：予算帯ごとの最速テキスト構成（実測と公称）"></p>


## 第 1 段階 · 2,500 ドルまで

*中古の 3090/4090、MI50/V100、Strix Halo、R9700* · 44 件


**📝 テキスト**

- **Bonsai-8B** · llama.cpp (PrismML fork) `1-bit Q1_0` — RTX 4090 → **368 tok/s** 📣 [出典](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 4090 24GB → **225 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-Flash-Next** · Strata `Strata· Swift 1.5 IQ2_XS` — RTX 4090 24GB + 32GB DDR5 → **220 tok/s** ✅ [出典](https://x.com/Knuckles_XBT/status/2105245662657011841)
- **Qwen3.6-35B-A3B** · FreeToken `FreeToken · NVFP4` — RTX 4090 → **167 tok/s** 🔁 [出典](https://x.com/shipfrontierai/status/2092602493213577481)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 3090 24GB → **154 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-27B** · DFlash `DFlash2` — RTX 3090 24GB → **138 tok/s** 🔁 [出典](https://x.com/yume_arasaki/status/2090971775714939097)
- **Bonsai-8B** · MLX `1-bit g128` — MacBook M4 Pro 48GB → **131 tok/s** 📣 [出典](https://huggingface.co/prism-ml/Bonsai-8B-mlx-1bit)
- **Qwen3.8-27B** · DFlash `EXL3 4.0bpw + DFlash2 3-bit…` — RTX 4090 24GB → **121 tok/s** ✅ [出典](https://x.com/yume_arasaki/status/2100595901006008791)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 3090 24GB → **120.8 tok/s** ✅ [出典](https://x.com/needmorevram/status/2105050786938118599)
- **Qwen3.8-Flash-Next** · Strata `Q2_0` — AMD Radeon AI PRO R9700 → **100 tok/s** ✅ [出典](https://x.com/TechPractice1/status/2105338176055509376) · [手順](recipes/x-009.ja.md)
- *…ほか 26 件は[エクスプローラー](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)で。*

**🖼️ 画像**

- **Qwen-Image 2.1** · ComfyUI `Comfy-Org INT8 · ComfyUI` — RTX 4090 24GB → 出典を参照 ✅ [出典](https://x.com/yume_arasaki/status/2102176739359404499) · [手順](recipes/image-001.ja.md)
- **Qwen-Image 2.1** `INT8` — RTX 3090 → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2102176739359404499)
- **Qwen-Image 2.1** · ComfyUI `ComfyUI` — Mac M4 Pro → 出典を参照 ✅ [出典](https://x.com/gabeciii/status/2104920039077884324)
- **Z-Image Turbo** · ComfyUI `ComfyUI` — RTX 3090 24GB → 出典を参照 ✅ [出典](https://x.com/michaelricks/status/2104959036353356058)

**🎬 動画・音声**

- **FastH3 V2 / Trim** `FP8` — RTX 4090 24GB → 出典を参照 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 4090 → 出典を参照 ✅ [出典](https://x.com/yume_arasaki/status/2097790831323427046)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 3090 → 出典を参照 ✅ [出典](https://x.com/natehalko/status/2103538997146611890)
- **ACE-Step 1.5** — RTX 3090 → 出典を参照 🔁 [出典](https://x.com/simplifyinAI/status/2091935190335754493)

## 第 2 段階 · 2,500〜7,000 ドル

*RTX 5090 1 枚、DGX Spark 1 台、Mac Studio Max* · 95 件


**📝 テキスト**

- **Qwen3.6-35B-A3B** · sparkinfer `sparkinfer v0.4.4` — RTX 5090 → **512 tok/s** 📣 [出典](https://x.com/kysstalol/status/2105042922643321008)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 5090 32GB → **283 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2) · [手順](recipes/hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.ja.md)
- **Qwen3.6-35B-A3B** · DFlash `DFlash 2` — Mac Studio M3 Ultra → **251 tok/s** ✅ [出典](https://x.com/tinybluedev/status/2089910202606764530)
- **Qwen3.8-Flash-Next** · Strata `IQ2_XS` — RTX 5090 + 256GB RAM → **176 tok/s** ✅ [出典](https://x.com/TechPractice1/status/2105087037363884483)
- **Qwen3.8-27B** · llama.cpp `GPU-1+ DFlash2` — RTX 5090 32GB → **176 tok/s** 📣 [出典](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- **Qwen3.8-27B** · llama.cpp `GPU-5+ DFlash2` — RTX 5090 32GB → **167 tok/s** 📣 [出典](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090 → **160 tok/s** 🔁 [出典](https://x.com/yume_arasaki/status/2107293459556225446)
- **Qwen3.8-Flash-Next** · Strata `Strata · IQ3_S` — RTX 5090+ 96GB DDR5-6400 → **150 tok/s** 🔁 [出典](https://x.com/kreia/status/2106054715373212025)
- **Qwen3.8-27B-NVFP4-MTP** · llama.cpp `LOW + MTP` — RTX 5090 32GB → **148.3 tok/s** 🔁 [出典](https://huggingface.co/esatapedico/Qwen3.8-27B-NVFP4-MTP-GGUF)
- **Qwen3.8-27B** · vLLM `NVFP4` — RTX 5090 32GB → **147 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2088734058842878037)
- *…ほか 67 件は[エクスプローラー](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)で。*

**🖼️ 画像**

- **Qwen-Image 2.1** `LightX2V / BennyDaBall NVFP…` — RTX 5090 32GB → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image 2.1** · TensorFold `TensorFold NVFP4 / FP8 / GG…` — RTX 5090 @450W → 出典を参照 ✅ [出典](https://x.com/niklaslenz_ai/status/2106465941177487871)
- **Qwen-Image 2.1** — RTX 5090 → 出典を参照 📣 [出典](https://x.com/fractalyze_io/status/2105207217452695841)
- **Qwen-Image 2.1** · SGLang `spark-image-lab BF16 / SGLa…` — 1× DGX Spark → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image-2.1-Turbo** `Turbo 8 vs Base 40` — RTX 5090 → 出典を参照 ✅ [出典](https://x.com/niklaslenz_ai/status/2108609693941920176)
- **Z-Image Turbo vs Qwen-Image 2.1** `prompt seed 20` — RTX 5090 → 出典を参照 ✅ [出典](https://x.com/princedoesai/status/2109376490009743713)

**🎬 動画・音声**

- **FastH3 V2** `NVFP4` — RTX 5090 32GB → 出典を参照 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/) · [手順](recipes/video-audio-001.ja.md)
- **FastH3 Trim** `NVFP4` — RTX 5090 → 出典を参照 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/)
- **FastH3 V2 / Trim** `NVFP4` — 1× / 2× DGX Spark → 出典を参照 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3** · ComfyUI `ComfyUI + SageAttention` — RTX 5090 → 出典を参照 ✅ [出典](https://x.com/RKAScope/status/2084359480926503182)
- **MiniMax H3 vs FastH3 Turbo** `seed` — RTX 5090 → 出典を参照 ✅ [出典](https://x.com/Sogni_Protocol/status/2097254959729246550)
- **MiniMax H3** · NVIDIA Sol `NVIDIA Sol` — 1× DGX Spark → 出典を参照 ✅ [出典](https://x.com/yume_arasaki/status/2100734364908986511)
- **MiniMax H3 vs LTX-2.3 Eros** `3 prompt` — 1× DGX Spark → 出典を参照 ✅ [出典](https://x.com/YRSM_Simon/status/2084222856972456336)
- **LTX-2.3** · ComfyUI `ComfyUI` — RTX 5090 → 出典を参照 ✅ [出典](https://x.com/freshstartsnow/status/2092263835591655773)
- **LTX-2.5** `LoRA` — RTX 5090 → 出典を参照 ✅ [出典](https://x.com/PhotogenicWeekE/status/2087298681137701274)
- **ACE-Step 1.5 + LTX-2.3** · ComfyUI `ComfyUI` — 1× DGX Spark → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2100734364908986511)
- **Wan2.1 14B** `97% + 3 + FP8` — RTX 5090 → 出典を参照 📣 [出典](https://x.com/thePandaily/status/2105209996648567243)
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s video + audio ≈72 s (steady state, excl. MP4 export; bas… 🏛️ [出典](https://x.com/LightX2V/status/2108769912009424976)

## 第 3 段階 · 7,000〜14,000 ドル

*DGX Spark 2 台、Mac Studio Ultra* · 23 件


**📝 テキスト**

- **Qwen3.8-Flash-Next 4/8-bit** · mlx-serve `4/8-bit mixed` — Mac Studio M5 Ultra 256GB → **126 tok/s** ✅ [出典](https://x.com/LocalSilicon/status/2106175358160793817)
- **DeepSeek-V4.1-Flash** · TensorFold — 2× DGX Spark → **95 tok/s** ✅ [出典](https://x.com/Urthoo/status/2106426248759005362)
- **DeepSeek-V4-Flash (0731 GA)** `FP8` — 2× DGX Spark → **82 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2083326111144906836)
- **Qwen3.8-Flash-Next** · TensorFold `TensorFold · NVFP4 / INT4-A…` — 2× DGX Spark → **67.4 tok/s** 🔁 [出典](https://x.com/llm_frontier_jp/status/2108884169069916440)
- **GLM-5.3-Flash EXL3** `EXL3` — 2× DGX Spark (GB10) → **61.43 tok/s** ✅ [出典](https://x.com/JASONMCNAB/status/2106367944963842279)
- **GLM-5.3-Flash EXL3 4-bit** · TensorFold `EXL3 4-bit` — 2× DGX Spark → **60.4 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2105598458547646875)
- **Qwen3.8-Flash-Next** · vLLM `NVFP4` — 2× DGX Spark → **54.4 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2094338533909475486)
- **GLM-5.3-Flash** · TensorFold — 2× DGX Spark → **54 tok/s** ✅ [出典](https://x.com/easthambuilds/status/2105693180427452703)
- **Qwen3.8-Flash-Next-hibrid48** · vLLM `NVFP4` — 2× DGX Spark → **51 tok/s** ✅ [出典](https://x.com/CryptoBandit100/status/2106374669477761493)
- **DeepSeek-V4.1-Flash** `Mia EXL3 2.9bpw · DSpark k=3` — 2× DGX Spark → **48.5 tok/s** ✅ [出典](https://x.com/yume_arasaki/status/2099966865326170554)
- *…ほか 13 件は[エクスプローラー](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)で。*

## 第 4 段階 · 14,000〜30,000 ドル

*Spark 3〜4 台のクラスター、マルチ GPU ワークステーション* · 10 件


**📝 テキスト**

- **Qwen3.8-27B** · SGLang `NVFP4` — RTX PRO 6000 → **300 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2090327658508763516)
- **GLM-5.3-Flash EXL3** · TensorFold `EXL3` — 4× DGX Spark → **95 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2108939694918488183)
- **Qwen3.8-Flash-Next** · Radiance (fork) `Radiance fork · int4fp8 · B…` — 4× AMD R9700 32GB + TR 9970X + 128GB → 出典を参照 🔁 [出典](https://x.com/richgel999/status/2109515169638326738)
- **Qwen3.8-27B** · Radiance (fork) `MXFP4 · Radiance fork` — 4× R9700 → 出典を参照 🔁 [出典](https://x.com/richgel999/status/2109515169638326738)
- **GLM-5.3-Flash** `Mia EXL3` — 3× DGX Spark → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2106837882870886438)
- **GLM-5.3-Flash** · TensorFold `TensorFold · Thunderbolt 5×…` — 2× Mac Studio M5 Ultra → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2108359576966094952)
- **DeepSeek-V4.1-Flash** `Mia MXFP4/FP8 · Engram NVMe` — 3× DGX Spark → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2099966865326170554)
- **DeepSeek-V4.1-Flash** · TensorFold `tonyd615 MXFP4 / Mia Tensor…` — 4× DGX Spark → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2106837882870886438)
- **DeepSeek-V4.1-Flash** — 4× DGX Spark → 出典を参照 🔁 [出典](https://x.com/hardfanaticos/status/2107225102475813374)
- **DeepSeek-V4.1-Flash** · MLX `MLX Q4i / DwarfStar` — M3 Ultra 512GB / M5 Max 128GB → 出典を参照 🔁 [出典](https://x.com/yume_arasaki/status/2099966865326170554)

## 価格非公開

1 枚単位で価格が出ているマルチ GPU 構成、価格の記載がない Mac など、単一の公開価格がないレシピ · 116 件。tok/s 上位のテキストレシピ：

- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 5080 16GB → **212 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.6-35B-A3B** · Splash `Splash` — Mac M5 Pro 48GB → **210 tok/s** 🔁 [出典](https://x.com/TeksEdge/status/2101735798567764421)
- **Qwen3.6-35B-A3B** · oMLX `oMLX 0.7.1.dev1` — Mac M5 Max → **205 tok/s** 🏛️ [出典](https://x.com/jundotkim/status/2108584837590495246)
- **Qwen3.8-Flash-Next-MLX-Serve-iQ-MLX-4.7bpw** · mlx-serve `iQ-MLX 4.7 bpw` — Mac Studio M5 Ultra → **157 tok/s** 📣 [出典](https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-iQ-MLX-4.7bpw)
- **Qwen3.8-27B** · vLLM `vLLM` — CMP 170HX → **147 tok/s** 🔁 [出典](https://x.com/LFrefman/status/2101572845017178243)
- **Qwen3.8-27B** · Splash `Splash` — Mac M5 Max → **144 tok/s** 🏛️ [出典](https://x.com/zhijianliu/status/2101102949158302001)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 5060 Ti 16GB → **128 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **GLM-5.3-Flash** `EXL3+ DS coordinator` — 4× DGX Spark + RTX 5090 → **124 tok/s** ✅ [出典](https://x.com/dangerm00se/status/2104876537367728325)
- **Qwen3.8-Flash-Next** · Strata `IQ3_S` — 2× RTX 3090 (48GB) + 64GB DDR5-6000 → **120 tok/s** ✅ [出典](https://x.com/geldeki/status/2109208295957201171) · [手順](recipes/x-004.ja.md)
- **Qwen3.8-Flash-Next** · Strata `q3 xs` — 2× Tesla V100 32GB PCIe → **120 tok/s** ✅ [出典](https://x.com/rewin123/status/2108669905616736529) · [手順](recipes/x-007.ja.md)
- **Ternary-Bonsai-2-27B-262k** · mirai-s-ada `Ternary Bonsai 2 27B + KV` — RTX 4070 12GB → **102 tok/s** 📣 [出典](https://huggingface.co/CaryPalmer/Ternary-Bonsai-2-27B-262k-GGUF)
- **Qwen3.8-Flash-Next** · Strata `Strata · Q2_0` — RTX 5070 12GB + Ryzen 5 7600 + 64GB DDR5 → **94 tok/s** 🏛️ [出典](https://github.com/Niko1221/Strata)
- *…全 116 件は[エクスプローラー](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)で見られます。*


## エンジンとツール

| プロジェクト                                                        | ⭐ Star | ライブ                                                                                             | 最終 push    | 概要                                                                                      |
| ------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------- |
| [llama.cpp](https://github.com/ggml-org/llama.cpp)            | 131.0k | ![stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat&label=)              | 2026-10-13 | GGUF の定番エンジン（CPU/CUDA/ROCm/Vulkan/Metal）。                                               |
| [vLLM](https://github.com/vllm-project/vllm)                  | 93.7k  | ![stars](https://img.shields.io/github/stars/vllm-project/vllm?style=flat&label=)               | 2026-10-13 | 高スループットな推論サーバー。Spark での MTP や同時実行のレシピに使われています。                                          |
| [SGLang](https://github.com/sgl-project/sglang)               | 37.1k  | ![stars](https://img.shields.io/github/stars/sgl-project/sglang?style=flat&label=)              | 2026-10-13 | 推論サービング用フレームワーク。DGX Spark で DFlash2 と組み合わせて使われています。                                     |
| [MLX](https://github.com/ml-explore/mlx)                      | 28.8k  | ![stars](https://img.shields.io/github/stars/ml-explore/mlx?style=flat&label=)                  | 2026-10-13 | Apple の配列フレームワーク。Mac のレシピの多くはこれがベース。                                                    |
| [Strata](https://github.com/Niko1221/Strata)                  | 23.5k  | ![stars](https://img.shields.io/github/stars/Niko1221/Strata?style=flat&label=)                 | 2026-10-12 | MoE のエキスパートを VRAM・RAM・SSD に分けて載せる推論エンジン。12〜24GB の GPU 向けで、ここの Flash-Next レシピの多くが使っています。 |
| [oMLX](https://github.com/jundot/omlx)                        | 22.8k  | ![stars](https://img.shields.io/github/stars/jundot/omlx?style=flat&label=)                     | 2026-10-13 | Apple Silicon 向けの MLX サーバー。連続バッチ処理と、KV/SSD の階層キャッシュに対応。                                 |
| [DFlash / DFlash 2](https://github.com/z-lab/dflash)          | 6.2k   | ![stars](https://img.shields.io/github/stars/z-lab/dflash?style=flat&label=)                    | 2026-08-18 | ブロック拡散による投機的デコーディング。DFlash 2 は Qwen3.8-27B 用のドラフトモデルを提供。                                |
| [LightX2V](https://github.com/ModelTC/LightX2V)               | 2.9k   | ![stars](https://img.shields.io/github/stars/ModelTC/LightX2V?style=flat&label=)                | 2026-10-13 | 動画生成の推論フレームワーク。RTX 5090 での MiniMax H3 の結果あり。                                            |
| [TensorFold](https://github.com/ashhart/TensorFold)           | 1.3k   | ![stars](https://img.shields.io/github/stars/ashhart/TensorFold?style=flat&label=)              | 2026-10-12 | OpenAI 互換 API の MoE ランタイム。投機的デコーディング付きで、ComfyUI の MiniMax H3 にも使われています。                 |
| [halogen](https://github.com/peonist-ai/halogen-flash-server) | 954    | ![stars](https://img.shields.io/github/stars/peonist-ai/halogen-flash-server?style=flat&label=) | 2026-10-13 | Strix Halo 向けにチューニングされた Flash-Next サーバー。                                                |
| [dflash-mlx](https://github.com/bstnxbt/dflash-mlx)           | 788    | ![stars](https://img.shields.io/github/stars/bstnxbt/dflash-mlx?style=flat&label=)              | 2026-08-20 | Apple Silicon（MLX）で動く DFlash 投機的デコーディング。                                                |
| [FastH3](https://haoailab.com/blogs/fasth3-rtx/)              | —      | *（サイト・ブログ）*                                                                                     | —          | Hao AI Lab による 8 ステップ蒸留版 MiniMax H3。RTX 向け（ブログ）。                                        |

<sub>⭐ スナップショットは `scripts/update_stars.py` で 2026-10-13T14:44Z（UTC）に更新 · 「ライブ」バッジは表示時に shields.io が描画します。</sub>

## 関連リスト・ベンチマーク

| プロジェクト                                                                      | ⭐ Star | ライブ                                                                                             | 最終 push    | 概要                             |
| --------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------- | ---------- | ------------------------------ |
| [Awesome-LLM-Inference](https://github.com/xlite-dev/Awesome-LLM-Inference) | 5.5k   | ![stars](https://img.shields.io/github/stars/xlite-dev/Awesome-LLM-Inference?style=flat&label=) | 2026-08-14 | 推論分野の論文とコードのまとめ。               |
| [awesome-local-llm](https://github.com/rafska/awesome-local-llm)            | 3.0k   | ![stars](https://img.shields.io/github/stars/rafska/awesome-local-llm?style=flat&label=)        | 2026-10-12 | ローカル LLM のプラットフォームとツールのまとめ。    |
| [LocalScore](https://github.com/cjpais/LocalScore)                          | 134    | ![stars](https://img.shields.io/github/stars/cjpais/LocalScore?style=flat&label=)               | 2026-10-09 | 1 GPU 向けの標準化されたベンチマーク CLI。     |
| [llamabench.ai](https://llamabench.ai/)                                     | —      | *（サイト・ブログ）*                                                                                     | —          | llama.cpp のベンチ結果を、起動コマンド付きで掲載。 |
| [llamaperf](https://llamaperf.com/leaderboard)                              | —      | *（サイト・ブログ）*                                                                                     | —          | コミュニティ投稿のリーダーボード（中央値で表示）。      |
| [canirun.ai](https://canirun.ai/)                                           | —      | *（サイト・ブログ）*                                                                                     | —          | 手持ちのハードでモデルが動くか、どれくらいの速度かを推定。  |

<sub>⭐ スナップショットは `scripts/update_stars.py` で 2026-10-13T14:44Z（UTC）に更新 · 「ライブ」バッジは表示時に shields.io が描画します。</sub>

## コントリビュート

1 レシピにつき 1 PR でお願いします。[投稿ページ](https://raytone-lab.github.io/Awesome-local-inference-recipe/submit.html)の YAML テンプレートをコピーし、出典に書かれている内容だけを埋めてください（それ以外は `null`）。`node scripts/validate.mjs` でチェックし、元の投稿へのリンクを添えてください。その後 `python3 scripts/gen_readme.py` で README をすべて再生成します。詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

ローカル開発：`python3 -m http.server 5190` → `index.html`（トップ）· `explore.html`（絞り込み・並べ替え・散布図）· スキーマは [`schema/recipe.schema.json`](schema/recipe.schema.json)。

<details><summary>サイトのプレビュー</summary>

<img src="docs/screenshot.png" width="760" alt="Awesome Local Inference Recipes">

</details>

## ライセンス

- コード：[MIT](LICENSE)
- データ（`data/`）：[CC BY 4.0](LICENSE-DATA)。Awesome Local Inference Recipes と、各レシピに記載された元の出典を明記すれば自由に再利用できます。
