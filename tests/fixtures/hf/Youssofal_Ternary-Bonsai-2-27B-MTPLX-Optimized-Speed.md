---
license: apache-2.0
library_name: mtplx
pipeline_tag: image-text-to-text
base_model:
- prism-ml/Ternary-Bonsai-2-27B-mlx-2bit
- Qwen/Qwen3.8-27B
base_model_relation: merge
tags:
- mlx
- apple-silicon
- macos
- speculative-decoding
- multi-token-prediction
- mtp
- mtplx
- local-ai
- local-llm
- llm
- coding
- vision
- ternary
- 2-bit
- bonsai
- prismml
- qwen3.8
- qwen3-8
- 27b
- m5
- m5-max
- m4
- m3
- macbook-air
- macbook-pro
- mac-mini
- opencode
- claude-code
---
**[MTPLX](https://mtplx.com): the fastest way to run Ternary Bonsai 2 27B on a Mac. Native multi-token-prediction speculative decoding on Apple Silicon, exact at any temperature.**

# Bonsai 2 27B Optimized Speed

**Prism ML ternary 27B model with vision and MTP. Compact weights for smaller Macs.**

Prism ML's Ternary Bonsai 2 27B is Qwen 3.8 27B rebuilt with ternary weights,
and Prism ML reports it keeps 98.2 percent of the full model's benchmark
average in 8.85 GB. On [MTPLX](https://mtplx.com) it runs on GPU kernels
written for it, with the Qwen 3.8 27B multi-token-prediction head drafting
ahead. That makes it faster than the 4-bit Qwen 3.8 27B in half the memory.
It reads images, and it runs on a Mac with 16 GB.

Prism ML's own figure for Bonsai 2 27B on an M5 Max with MLX is 46.8 tok/s.
On MTPLX the same chip decodes it at 64.4 tok/s after a 4,061-token prompt.

## Measured on MTPLX 2.12.0 (22 September 2026)

This is the Bonsai 2 27B MLX pack for MTPLX, the fastest way to run Bonsai 2
on a Mac. MacBook Pro M5 Max with 128 GB, sampled at the model's own settings
(temperature 1.0, top-p 0.95, top-k 20), thinking off, 512 generated tokens,
one model loaded at a time.

| Prompt | Bonsai 2 27B Optimized Speed | Qwen 3.8 27B Optimized Speed | Peak memory, Bonsai and 27B |
|---|---:|---:|---:|
| 4,061 tokens | 64.4 tok/s | 52.6 tok/s | 11.4 and 23.9 GB |
| 16,350 tokens | 57.1 tok/s | 51.0 tok/s | 14.6 and 27.0 GB |

Runs on Apple Silicon Macs with 16 GB of unified memory or more. From MTPLX
2.12.0 it is the first recommendation on M3, M4 and M5 Macs with 16 to 31 GB.

## How it is built

- Prism ML stores every weight of the language model as −1, 0 or +1 with one
  scale per group, so the 27B language model takes 7.67 GB.
- MTPLX runs those weights natively, with GPU kernels for Prism ML's rotation
  and for the ternary matrix multiply.
- The Qwen 3.8 27B multi-token-prediction head drafts ahead, and the full
  model verifies its drafts in one pass.
- The Qwen 3.8 27B vision tower is included.

| | |
|---|---|
| Download | 8.85 GB |
| Peak while serving | 11.4 GB at a 4K prompt, 14.6 GB at 16K |
| Recommended Macs | 16 GB+ unified memory (18 GB+ for agent clients such as OpenCode) |
| Context window | 8,192 tokens on 16 GB, 20,480 on 18 GB, 94,208 on 24 GB, up to 262,144 |
| MTP depth | 1 |
| Reasoning effort | medium by default, xhigh available |
| Sampling | temperature 1.0, top-p 0.95, top-k 20 |

The serving contract ships inside `mtplx_runtime.json`. MTPLX reads it on
load. Drafts are accepted with the probability-ratio rule plus residual
resampling, so the output follows the model's own distribution at any
temperature.

## Use it

Mac app (MTPLX 2.12.0 or later): download at
[mtplx.com](https://mtplx.com), pick "Bonsai 2 27B Optimized Speed".

Command line (MTPLX 2.12.0 or later):

```bash
pip install mtplx
mtplx serve --model Youssofal/Ternary-Bonsai-2-27B-MTPLX-Optimized-Speed
```

Siblings: [Qwen 3.8 27B Optimized Speed](https://huggingface.co/Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed)
(the 4-bit 27B, for Macs with 32 GB or more) and
[MiMo V2.6 Qwen 9B Optimized Speed](https://huggingface.co/Youssofal/MiMo-V2.6-Qwen-9B-MTPLX-Optimized-Speed).

Base model: [prism-ml/Ternary-Bonsai-2-27B-mlx-2bit](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit),
built from [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)
(Apache 2.0; `LICENSE` and `NOTICE.txt` in this repo). Created using Bonsai by
Prism ML.
