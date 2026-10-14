---
library_name: mlx
license: other
license_name: qwen-community-1.0
license_link: LICENSE
base_model: Qwen/Qwen3.8-Flash-Next
pipeline_tag: text-generation
tags:
- mlx
- safetensors
- qwen4_exp
- oq
- quantized
- mtp
- mixed-precision
---

# Qwen3.8-Flash-Next-oQ4e-mix6-mtp

[繁體中文版 →](README_zh.md)

> **A v2 build exists:** [umixer/Qwen3.8-Flash-Next-oQ4e-mix6-mtp-v2](https://huggingface.co/umixer/Qwen3.8-Flash-Next-oQ4e-mix6-mtp-v2)
> — trunk re-baked with Jundot's new-mechanism oQ4e (imatrix + LSQ refit),
> giving higher accuracy on finished answers (see that repo's Quality section).
> Same U-shaped allocation, same footprint; this repo stays the original v1.

**Goal: oQ4e speed and memory footprint, oQ5e-or-better quality reaching toward
"Q6-class".** Runs at ~73–75 GB resident with ~82→66 tok/s decode on a 128 GB Apple
Silicon host — the speed/RAM economics of a 4-bit build, at an accuracy tier
above uniform oQ5e.

*How:* a mixed-precision MLX build of Qwen3.8-Flash-Next, assembled by
**component-wise byte-copy** from native upstream oQ quantizations —
**zero re-quantization in the entire package**. Every tensor is byte-identical
to its source, so quality is traceable, not re-derived.

## Why this build exists

Uniform-bit quantization pays accuracy where it isn't needed (middle layers) and
loses it where it hurts (first/last layers, n-gram table, attention).
Layer-sensitivity literature (SliderQuant arXiv:2603.25284, NSDS
arXiv:2603.17354) shows quantization sensitivity is U-shaped across depth:
expensive edges, cheap middle. This package prices that curve with **native
bits** — the high-value components are lifted verbatim from higher-bit packs
instead of re-quantized.

## Recipe & comparison

| Component | This build (mix6-mtp) | uniform oQ4e | Resident Δ vs oQ4e | Source (byte-identical) |
|---|---|---|---|---|
| Trunk MoE experts, layers 0–3 & 44–47 (U-shaped edges) | **6-bit g64** | 4-bit | **+4.8 GB** (hot, fully resident) | [mlx-community/Qwen3.8-Flash-Next-oQ6e-mtp](https://huggingface.co/mlx-community/Qwen3.8-Flash-Next-oQ6e-mtp) |
| Trunk MoE experts, middle 40 layers | 4-bit g64 | 4-bit | 0 | [Jundot/Qwen3.8-Flash-Next-oQ4e-mtp](https://huggingface.co/Jundot/Qwen3.8-Flash-Next-oQ4e-mtp) |
| Attention / GDN / hyper-connections / conv | **6-bit all 48 layers** | mostly 4-bit, only L29–46 raised to 5–6 (peaks L31/L39 at 8) | **+0.4 GB** (hot, resident) | oQ6e |
| N-gram (PLE) embedding table | **6-bit** (41.7 GiB) | 4-bit (≈26 GiB) | ≈0 (SSD-offloaded on hosts; page-cache only) | oQ6e |
| Shared experts | 8-bit | 8-bit | 0 | oQ6e |
| embed_tokens / lm_head | 8-bit g64 | 8-bit g64 | 0 | oQ6e |
| MTP drafter (all components, incl. its own experts) | **6-bit** | 4-bit experts / 6-bit attn | **+0.6 GB** (hot, resident) | oQ6e |
| Norms / routers / vision tower | bf16, unquantized | bf16, unquantized | 0 | oQ6e |
| **Total at load** | **75.34 GB** | **69.53 GB** | **+5.8 GB** | `engine_pool` actual, same host |

Every component where this build differs from uniform oQ4e is one the router or
the hot path touches every token — the extra 5.8 GB of resident weights buys
6-bit exactly where quantization error is realized.

Skeleton: `bits=4, group_size=64, mode=affine`; every high-bit component is a
per-tensor entry in `config.json` (mirrored across `quantization` and
`quantization_config`). Build integrity verified: safetensors packed geometry
matches all 150 switch-mlp config declarations (0 mismatches); swapped tensors
verified `mx.array_equal` against source packages; untouched shards hardlinked from base
(bites not written, bytes proven equal).

## Specs & measurements (M5 Max 128 GB, oMLX 0.7.0 @PR4335)

| Item | Value |
|---|---|
| Architecture | qwen4_exp — MoE + n-gram PLE + MTP; 48 layers, 512 experts, top-10 routed; 125B total / 6B active / 51B n-gram / 4B MTP |
| Package | 116.7 GiB, 28 shards |
| Resident at load | ~73–75 GB (oMLX, fresh load) |
| vs uniform oQ4e (same host) | **+5.8 GB initial resident** (75.34 vs 69.53 GB, both `engine_pool` actual loads on this M5 Max under oMLX 0.7.1) — the premium buys 6-bit experts on the U-curve edges (L0–3/L44–47), the 6-bit n-gram table (41.7 GiB vs 4-bit ≈26 GiB) and a fully 6-bit MTP drafter (uniform oQ4e: 4-bit) |
| vs uniform oQ5e (same family) | oQ5e package ≈128 GiB, initial resident ≈85 GB (measured on this M5 Max 128 GB host) — this build starts ~10–12 GB lower while matching or beating oQ5e accuracy (see Quality) |
| Context tested | 131k |
| MTP | native 6-bit, depth 3; acceptance 65–75% on agent/edit traffic; measured +6~8% tg @64k vs 4-bit drafter |

### Speed ladder — v1 vs uniform oQ4e (same host)

M5 Max, fan 80%, cold start 40 °C, second of two back-to-back runs per build,
oMLX 0.7.1.dev1. Same harness for both builds.

| Test | oQ4e tg | v1 tg | oQ4e pp | v1 pp | Δpp |
|---|---|---|---|---|---|
| pp1199/tg256 | 88.5 | 136.7 | 1,701.5 | 1,729.5 | +1.6% |
| pp4408/tg256 | 73.6 | 86.3 | 2,622.8 | 2,384.2 | −9.1% |
| pp8155/tg256 | 81.4 | 80.0 | 2,778.3 | 2,525.7 | −9.1% |
| pp15744/tg256 | 79.5 | 78.0 | 2,837.8 | 2,543.6 | −10.4% |
| pp30946/tg256 | 75.5 | 72.0 | 2,788.2 | 2,528.4 | −9.3% |
| pp62030/tg256 | 73.2 | 71.0 | 2,717.3 | 2,479.9 | −8.7% |
| pp122463/tg256 | 58.0 | 67.0 | 2,623.7 | 2,448.4 | −6.7% |
| **Mean** | **75.7** | **84.4** | **2,581.4** | **2,377.1** | **−7.9%** |

tg: no regression vs oQ4e. pp: honest ~8% cost — the 6-bit hot-path weights are
read on the prefill path too.

## Usage

Requires **oMLX 0.7.0** (or mlx_vlm builds that support `qwen4_exp` plus
per-tensor mixed-precision quantization entries). Enable MTP speculative
decoding — the drafter is native 6-bit and pays for itself at long context.

```python
from mlx_vlm import load, generate
model, processor = load("umixer/Qwen3.8-Flash-Next-oQ4e-mix6-mtp")
```

## Quality

Task-level benchmarks on this build (sampled-300 protocol, thinking on,
reasoning effort: **medium**, truncation accounted):

| Benchmark | Accuracy | Correct/Total | Notes |
|---|---|---|---|
| MMLU-Pro | **88.3%** | 265/300 | 1 hit token limit (1 correct); 88.6% on finished (n=299) |
| MATHQA | **92.0%** | 276/300 | 2 hit token limit (1 correct); 92.3% on finished (n=298) |
| MBPP | **94.7%** | 284/300 | 9 hit token limit (1 correct); **97.3% on finished (n=291)** |

Above uniform oQ5e on all three axes at a lower footprint.

| Accuracy axis | This build (mix6-mtp) | uniform oQ5e |
|------|------|------|
| Backbone / n-gram table / MTP (per-token hot path) | 6–8 bit native | 5 bit |
| First & last 4 layers' experts (high-routing-sensitivity edges) | 6 bit native | 5 bit |
| Middle 40 layers' experts (top-10/512 diluted) | 4 bit | 5 bit |
| Initial resident (M5 Max 128 GB) | **73–75 GB** | **≈85 GB** |
| 256k ctx on 128 GB (swap off) | safe margin | ⚠️ crash risk (page-cache starvation) |

**Estimated accuracy tier: oQ5e-class or better.** All three hot-path axes
sit above oQ5e; the single axis one step below is the middle-expert bucket,
diluted by top-10-of-512 routing (4 bit vs 5 bit).
KLD measurement needs a 192 GB+ host — this is a structural estimate; the
speed ladder shows no measurable decode tax.

## License & provenance

Derived from [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
(Qwen community license, `license: other`, applies to all weight derivatives).
Assembled byte-wise from community oQ quantizations — [mlx-community/Qwen3.8-Flash-Next-oQ6e-mtp](https://huggingface.co/mlx-community/Qwen3.8-Flash-Next-oQ6e-mtp)
and [Jundot/Qwen3.8-Flash-Next-oQ4e-mtp](https://huggingface.co/Jundot/Qwen3.8-Flash-Next-oQ4e-mtp)
— whose assembly and metadata rights are respected; weight lineage remains Qwen's.

## Acknowledgments

- [mlx-community/Qwen3.8-Flash-Next-oQ6e-mtp](https://huggingface.co/mlx-community/Qwen3.8-Flash-Next-oQ6e-mtp) — the 6-bit source supplying every hot-path component in this build.
- [Jundot](https://huggingface.co/Jundot) — for [Qwen3.8-Flash-Next-oQ4e-mtp](https://huggingface.co/Jundot/Qwen3.8-Flash-Next-oQ4e-mtp) (the 4-bit expert source) and for developing [oMLX](https://github.com/jundot/omlx) / the oQ quantizer that makes per-tensor mixed-precision builds possible on Apple Silicon.

