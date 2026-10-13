<div align="center">

# ⚡ RecipeBench

**Local inference recipes — model × engine × hardware, every number sourced.**
**本地推理配方库：跨引擎、消费级/二手硬件、每个数字标来源、聚焦 ≤ $30k**

![recipes](https://img.shields.io/badge/recipes-176-4f46e5) ![license](https://img.shields.io/badge/license-TBD-lightgrey) ![PRs welcome](https://img.shields.io/badge/PRs-welcome-16a34a) ![data](https://img.shields.io/badge/data-2026--10--13-orange)

<img src="docs/screenshot.png" width="860" alt="RecipeBench landing page">

</div>

> **RecipeBench** is a working name (placeholder). / 项目名为暂定名。

## What & why

On the same RTX 5090, Qwen3.8-Flash-Next runs at **~15 tok/s** on stock llama.cpp and **~160–176 tok/s** with Strata. On local hardware, the *recipe* (quant + engine + flags) matters more than the card. Existing leaderboards cover one engine (llamabench), self-reported medians without recipes (llamaperf), or estimates (canirun). RecipeBench collects:

- **Cross-engine recipes**: Strata, oMLX, DFlash2, MTP, TensorFold, LightX2V, llama.cpp, vLLM, SGLang…
- **Consumer & used hardware**: RTX 3090/4090/5090, DGX Spark clusters, Mac Studio/mini, Strix Halo, used V100/MI50
- **Text, image, and video+audio models**
- **Cost-aware**: hardware price, `$ per tok/s`, budget tiers up to $30k
- **Every number has a source link and evidence level.** Unknowns stay `null`. Nothing is estimated.

## 🔥 Hot recipes on X (2026-09-15 → 10-13)

| Model | Engine · Quant | Hardware | Result | Level | Post |
|---|---|---|---|---|---|
| Qwen3.8-Flash-Next | Strata v0.1.27 · IQ2_XS | RTX 5090 + 256GB RAM | **176 tok/s** decode, 5,247 prefill, 128K | 实测 | [@TechPractice1](https://x.com/TechPractice1/status/2105087037363884483) |
| Qwen3.8-Flash-Next | Strata v0.1.42 · IQ3_S | 2× RTX 3090 + 64GB | **120+ tok/s** sustained (peak 153), 262K | 实测 | [@geldeki](https://x.com/geldeki/status/2109208295957201171) |
| Qwen3.8-Flash-Next | Strata · q3 xs | 2× V100 32GB (used) | **120 tok/s** (llama.cpp 30) | 实测 | [@rewin123](https://x.com/rewin123/status/2108669905616736529) |
| Qwen3.8-Flash-Next | Strata · IQ3_XXS | RTX 4090, 131K ctx | **78.6 tok/s**, 887 prefill | 实测 | [@BrianMRey](https://x.com/BrianMRey/status/2103789711311413320) |
| Qwen3.8-Flash-Next | Strata / halogen · IQ4_XS | Strix Halo 395 | **47.7** / 34.3 tok/s (llama.cpp 23.2) | 实测 | [@no_stp_on_snek](https://x.com/no_stp_on_snek/status/2108296174994088177) |
| Qwen3.8-Flash-Next | Strata 0.1.39 · IQ3_S | 2× MI50 32GB (used) | **50 tok/s** (llama.cpp 37) | 实测 | [@sami3dat](https://x.com/sami3dat/status/2106815932521971964) |
| GLM 5.3 | oMLX (tuned) | Mac Studio M5 Ultra | **87** prose / 125 code tok/s | 实测 | [@JamesMcPherson](https://x.com/JamesMcPherson/status/2104028051285672431) |
| GLM-5.3-Flash | TensorFold 0.5 + DFlash2 | 2× DGX Spark TP2 | **54 tok/s** 1 stream, 142 total @4 | 实测 | [@easthambuilds](https://x.com/easthambuilds/status/2105693180427452703) |
| MiniMax H3 | TensorFold (ComfyUI) | RTX 5070 Ti 16GB | 1344×768 5s: **81 s** (stock 623 s) | 实测 | [@jayleaton](https://x.com/jayleaton/status/2106213885917491367) |
| MiniMax H3 | LightX2V | RTX 5090 | 768×1344 15s video+audio: **~72 s** | 官方 | [@LightX2V](https://x.com/LightX2V/status/2108769912009424976) |

## Source levels / 来源等级

| Level | Meaning |
|---|---|
| **官方** Official | Published by the project or vendor (usually best case) |
| **实测** Measured | Author ran it on their own machine, with screenshot or log |
| **转述** Relayed | Second-hand quote; check the original post |
| **宣称** Claimed | Projection or no reproducible conditions |

## Data schema

One recipe per record (`data/recipes.json` today, `recipes/*.yaml` planned). Full schema: [`schema/recipe.schema.json`](schema/recipe.schema.json).

```yaml
id: text-qwen38-flashnext-2x3090-strata
category: text              # text | image | video-audio
model: Qwen3.8-Flash-Next
quant: IQ3_S
engine: Strata v0.1.42      # engine + version
hardware: 2× RTX 3090 + 64GB DDR5
hardware_family: NVIDIA 消费级  # Mac | NVIDIA 消费级 | DGX Spark | AMD | 二手数据中心卡 | 其他
hardware_cost_usd: null     # unknown → null, never estimate
metric: "120+ tok/s sustained decode; 2,844 tok/s cold prefill"
tok_s: 120                  # single-stream generation only (not prefill, not aggregate)
concurrency: null
context: 262K
launch_command: null        # only if shown in the source
source_url: https://x.com/geldeki/status/2109208295957201171
source_level: 实测
date: 2026-10-11
```

## Contribute / 贡献

1. Fork → add one recipe (template on the site's 提交配方 page)
2. `node scripts/validate.mjs`
3. Open a PR with the source link (and your command + output for self-measured runs)

Rules: no estimates, link and summarize posts (don't copy them in full). See [CONTRIBUTING.md](CONTRIBUTING.md).

## Local dev

Plain static site, no build step:

```bash
python3 -m http.server 5190 --bind 127.0.0.1   # → http://127.0.0.1:5190
node scripts/validate.mjs                        # schema check
```

Pages: `index.html` (landing) · `explore.html` (filterable table, drawer, scatter) · `submit.html`.

## Roadmap

- [ ] Split data into `recipes/*.yaml` + build step → JSON
- [ ] CI: validate on every PR, deploy to GitHub Pages
- [ ] Launch commands for top recipes (currently none captured)
- [ ] Concurrency/aggregate throughput as a separate field
- [ ] Image/video metrics normalized (seconds per output-second at a resolution)
- [ ] Price snapshots with dates, auto-refresh
- [ ] "Reproduced by" counter for recipes verified by multiple people

## 中文简介

RecipeBench 收集社区真实跑出的本地推理配方：模型、量化、引擎、硬件、速度、成本、上下文。每条数据都带原帖链接和来源等级（官方 / 实测 / 转述 / 宣称），未知字段显示「未见公开数据」。聚焦消费级显卡、DGX Spark、Mac 和二手数据中心卡，预算 ≤ $30k。欢迎通过 PR 提交配方。

## License

**Not chosen yet.** Suggestion: MIT for code, **CC BY 4.0** for `data/`, so others can reuse the data with attribution.
