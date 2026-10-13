---
license: apache-2.0
pipeline_tag: text-generation
library_name: mlx
tags:
- mlx
- turboquant
- quantization
- apple-silicon
- moe
- gpt-oss
base_model: openai/gpt-oss-20b
---

# gpt-oss-20b-tq3

**TurboQuant 3-bit MLX quantization** of [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) — produced with [TurboQuant-MLX](https://github.com/manjunathshiva/turboquant-mlx).

GPT-OSS-20B is a 21 B-parameter Mixture-of-Experts model with 32 experts and ~3.6 B active parameters per token. After TurboQuant 3-bit compression it fits comfortably on a **16 GB Apple Silicon Mac** with full 131K-token context — and with the v0.2 KV-cache compression layered on top, the cache shrinks 4× as well.

## Model Details

- **Base Model**: [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) (21 B total, 32 experts, ~3.6 B active)
- **Quantization**: TurboQuant 3-bit (Hadamard rotation + Lloyd-Max codebook), `group_size=64`
- **Calibration data**: **none** — TurboQuant is data-free
- **Size**: ~9.5 GB on disk
- **Peak wired RAM at decode**: ~11 GB (verified on a 16 GB Mac with macOS background apps)
- **Decode speed**: 60–80 tok/s (M-series), up to 73 tok/s on M4 Max with fp16 KV cache
- **Runs on**: Apple Silicon (M1/M2/M3/M4) with 16 GB or more unified memory
- **No streaming needed**: at ~9.5 GB this runs **fully resident** on 16 GB+ — expert streaming (for MoEs too big for RAM) would only add disk reads and slow it down. Resident is always the fast path for a model this size.

<!-- turboquant-plan:begin -->

## Will it fit my Mac?

Don't guess, and don't download **9.9 GB** to find out — ask first (needs `turboquant-mlx-full >= 0.15.1`):

```bash
turboquant-plan --model manjunathshiva/gpt-oss-20b-tq3
```

It reads **only this repo's safetensors headers over the network** (a couple of hundred KB, a few seconds — the weights are never fetched), then projects the peak against *your* machine and prints the flags to use:

```
Model
  weights (exact)      9.9 GB
  KV cache             24.4 KB/token  (hybrid: 12/24 full-attention, 12 sliding (window 128))

Verdict: <resident | needs a wired-limit raise | streaming>
Recommended: <the exact flags for your Mac>
```

Planning for a machine you're **not sitting at** — deciding whether a 16 GB mini or a 64 GB Mac can take this — is what `--wired-gb` / `--ram-gb` are for:

```bash
turboquant-plan --model manjunathshiva/gpt-oss-20b-tq3 \
    --wired-gb 10.5 --ram-gb 16 --context 8192
```

`turboquant-doctor` runs the same projection plus a readiness check; both take `--json`. The projection is calibrated against real measurements on a 16 GB Mac mini rather than estimated from theory — on the [9.4 GB ternary 35B](https://huggingface.co/manjunathshiva/Qwen3.6-35B-A3B-tq3a-tqTe-g64) it predicts a 10.44 GB peak where that machine measures 10.42.

<!-- turboquant-plan:end -->

## Requirements

```bash
pip install "turboquant-mlx-full>=0.2.0" "mlx-lm>=0.31.3"
```

## Sampler recommendations

GPT-OSS-20B is a sub-25B model, which means it sits right at the edge of capability for multi-step reasoning. Sampler choice matters more here than on larger models:

| Use case | Recommended sampler |
|---|---|
| **Casual chat / creative writing / Q&A** | `--temp 0.7 --rep-penalty 1.1` |
| **Math, code, multi-step reasoning** | `--temp 0.3 --rep-penalty 1.1` |

At temp 0.7 the model occasionally gives up mid-problem on word problems, or writes plausible-looking but logically buggy code. Dropping to temp 0.3 stabilizes the reasoning trace and produces correct setups for both math and code.

## Verified quality (6-test stress harness)

Tested with `scripts/stress_hybrid_sampler.py` on a 64 GB M-series Mac (peak RAM matches 16 GB target):

| # | Test | Verdict (recommended sampler) |
|---|---|---|
| 01 | long_essay (1500-word Roman Empire, 3500 max_tok) | clean, no degenerate tail |
| 02 | math (two trains, meeting time + distance, 800 max_tok) | correct at `--temp 0.3` (sets up `60t + 75(t-0.5) = 215`, solves t≈1.87 hr → 10:52 AM); unstable at temp 0.7 |
| 03 | code (`merge_intervals` + 3 unit tests, 1500 max_tok) | correct function logic at `--temp 0.3`; occasional hallucinated assertion values (function works, fix the test) |
| 04 | needle (FUCHSIA-7741 in haystack, 200 max_tok) | password retrieved verbatim |
| 05 | format (5-item list under 15 words/line, 1500 max_tok) | exactly 5 short numbered lines, no commentary |
| 06 | repetition_trap (sky-blue thorough, 4096 max_tok) | clean answer, no paragraph loops |

Decode speed across all 6 tests: 46–94 tok/s. Peak RAM: 11.0–11.2 GB.

## Quick Start

### Download the model

```bash
hf download manjunathshiva/gpt-oss-20b-tq3 \
    --local-dir ~/models/gpt-oss-20b-tq3
```

### Generate text — standard chat

```bash
turboquant-generate \
    --model ~/models/gpt-oss-20b-tq3 \
    --prompt "Why is the sky blue? Explain in detail." \
    --max-tokens 1024 --temp 0.7 --rep-penalty 1.1
```

### Generate text — math / code (temp 0.3)

```bash
turboquant-generate \
    --model ~/models/gpt-oss-20b-tq3 \
    --prompt "Solve this multi-step word problem..." \
    --max-tokens 1024 --temp 0.3 --rep-penalty 1.1
```

### Generate with TurboQuant KV cache (v0.2+) — 4× smaller cache

For long-context generation, layer the v0.2 KV-cache compression on top. **K8/V3 mixed precision is required** when stacking on TurboQuant-quantized weights — symmetric `K3` would compound the noise and break long-form output past ~800 tokens. The 128-token fp16 sink protects attention sinks at the prompt start.

```bash
turboquant-generate \
    --model ~/models/gpt-oss-20b-tq3 \
    --prompt "Why is the sky blue? Explain in detail." \
    --max-tokens 1024 --temp 0.7 --rep-penalty 1.1 \
    --kv-k-bits 8 --kv-v-bits 3 --kv-min-tokens 128
```

## Serve over an OpenAI-compatible API

Run it as a drop-in `mlx_lm.server` replacement — `turboquant-serve` patches the
loader so the TurboQuant weights load through the PolarQuant path, then exposes the
standard OpenAI endpoints:

```bash
turboquant-serve --model manjunathshiva/gpt-oss-20b-tq3 --port 8080
```

Call it from any OpenAI-compatible client (the `model` field must match the
`--model` string):

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "manjunathshiva/gpt-oss-20b-tq3",
       "messages": [{"role": "user", "content": "Why is the sky blue?"}],
       "max_tokens": 1024, "temperature": 0.7}'
```

Or from Python via the OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")
resp = client.chat.completions.create(
    model="manjunathshiva/gpt-oss-20b-tq3",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    max_tokens=1024, temperature=0.7,
)
print(resp.choices[0].message.content)
```

All `mlx_lm.server` flags forward unchanged (`turboquant-serve --help`). Note: `mlx_lm.server` is for development/local use — no authentication or rate limiting.

## License

Apache-2.0 (inherited from the base model).

## Citation & Project

Built with [TurboQuant-MLX](https://github.com/manjunathshiva/turboquant-mlx). For the science (Hadamard rotation + Lloyd-Max codebooks for data-free quantization), see [Zandieh et al., 2025 — TurboQuant: Online Vector Quantization with Optimal Distortion-Rate Trade-off](https://arxiv.org/abs/2504.19874).
