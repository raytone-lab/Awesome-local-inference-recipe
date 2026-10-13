---
license: apache-2.0
base_model:
- Qwen/Qwen3.6-35B-A3B
base_model_relation: quantized
pipeline_tag: text-generation
language:
- en
tags:
- mixture-of-experts
- moe
- qwen3
- 2-bit
- quantization
- eschamoe
- sglang
- zml
- mlx
- apple-silicon
- macos
- metal
- code
- reasoning
- conversational
metrics:
- accuracy
- code_eval
model-index:
- name: Qwen3.6-35B-A3B-Escha-W2
  results:
  - task: {type: text-generation, name: Code Generation}
    dataset: {type: evalplus/humanevalplus, name: HumanEval+}
    metrics:
    - {type: pass@1, value: 92.07, name: pass@1 (greedy, thinking-off)}
  - task: {type: text-generation, name: Code Reasoning}
    dataset: {type: cruxeval, name: CRUXEval-O}
    metrics:
    - {type: accuracy, value: 61.75, name: acc (n=800)}
  - task: {type: text-generation, name: Code Generation}
    dataset: {type: livecodebench, name: LiveCodeBench v6 (release_v6, N=182 subset)}
    metrics:
    - {type: pass@1, value: 62.64, name: pass@1 (subset — retention vs FP8)}
  - task: {type: text-generation, name: Commonsense Reasoning}
    dataset: {type: commonsense, name: Commonsense-6 (avg)}
    metrics:
    - {type: accuracy, value: 76.06, name: avg acc (thinking-off)}
  - task: {type: text-generation, name: Knowledge & Reasoning}
    dataset: {type: TIGER-Lab/MMLU-Pro, name: MMLU-Pro}
    metrics:
    - {type: accuracy, value: 80.9, name: acc (5-shot CoT, thinking-on)}
  - task: {type: text-generation, name: Math Reasoning}
    dataset: {type: math-500, name: MATH-500}
    metrics:
    - {type: accuracy, value: 93.8, name: acc (thinking-on, budget-capped)}
  - task: {type: text-generation, name: Graduate-level Science}
    dataset: {type: gpqa, name: GPQA-Diamond}
    metrics:
    - {type: accuracy, value: 77.8, name: acc (thinking-on)}
---

# Qwen3.6-35B-A3B-Escha-W2 — 2-bit quantized (`eschamoe`)

By **[Escha Labs Inc.](https://eschalabs.com/)**

**Escha-W2** is a 2-bit quantized build of **Qwen3.6-35B-A3B**, a Mixture-of-Experts model with
256 experts, packaged with everything needed to serve it locally through an **OpenAI-compatible
HTTP API**. (The runtime and served model id keep the `escha` name — see *Connecting a client*.)

The whole thing is **12.3 GB on disk** and runs on a **single 24 GB consumer GPU** — or on a
**16 GB card** (e.g. RTX 5060 Ti), where you trade concurrency *or* context, not both[^ctxcap].

| | |
|---|---|
| Base model | Qwen3.6-35B-A3B (MoE, 256 experts) |
| Quantization | 2-bit experts (`eschamoe`; mixed 2/3-bit per projection), int8 dense layers |
| Size on disk | 12.3 GB |
| Minimum GPU | **16 GB** VRAM (fewer concurrent streams, or less context — your choice[^ctxcap]), **24 GB** recommended; NVIDIA Ampere (sm_80) → Blackwell (sm_120) |
| Platform | Linux x86-64, **glibc ≥ 2.28** (Ubuntu 20.04+, RHEL/Rocky/Alma 8+) — the wheel is `manylinux_2_28` |
| CUDA | an NVIDIA **driver** — no CUDA toolkit needed (`ptxas` ships inside `triton`, a PyTorch dependency) |
| Python | **3.12**, for the SGLang engine — the ZML engine needs no Python at all |
| Interface | OpenAI-compatible `/v1` on port 30000 |

---

## Contents

| Path | What it is |
|---|---|
| `*.safetensors`, `config.json`, `tokenizer*`, `vocab.json`, `merges.txt`, `*.jinja` | the quantized weights, tokenizer and config (at the repo root) |
| `opencode.json` | example client config (see *Connecting a client*) |
| `LICENSE`, `THIRD_PARTY_LICENSES/` | Apache-2.0 plus the upstream license texts |

This repo holds **only the model**. The **runtimes** live in a separate repo,
**[EschaLabs/escha-runtime-qwen3moe](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe)**,
one directory per engine: **`sglang/`** (the `escha` wheel + `serve.sh` — servers, concurrency,
tools, structured output) and **`zml/`** (a single-binary runtime — no Python, no dependencies,
and the stronger single-user decode on most cards).

On **Apple Silicon**, [escha-mlx](https://github.com/EschaLabs/escha-mlx) serves these weights
natively on MLX. It reads this repo directly, with no conversion step. See
[Apple Silicon (MLX)](#apple-silicon-mlx) below.

### Which engine?

**Use `sglang/` unless you have a specific reason not to.** It is the engine every number on this
page was measured with, and the only one that supports concurrency, tool calling, structured
output and a reasoning parser.

Choose `zml/` when you want a single-user box with **no Python at all** — one binary, no venv, no
CUDA toolkit, 14-second install — and you generate long answers. It is the only way to run this
model without a Python environment.

Two things decide whether that trade is worth it on **your** box:

- **The decode lead is card-dependent.** On answers ≥1k tokens, measured 2026-07-27: **+15–26%**
  on an RTX 5090 or 3090, **+8–11%** on a 5080, **+2–5%** on a 4090 (against a fully tuned SGLang),
  and a **tie** on a 5060 Ti. ZML loses short replies on every card, and its first start compiles
  graphs — 75–145 s on a 4090, minutes on a 16 GB card, versus ~33 s for SGLang.
- **The lead is greedy-only.** ZML's fast path fuses 16 decode steps per GPU dispatch with
  on-device argmax; any `temperature > 0` falls back to a per-token loop that is **~2.15× slower**
  (RTX 4090, 512-token answer: 218 tok/s at `temperature: 0` vs 102 at `0.6`). Send
  `"temperature": 0` for the quoted numbers — including with `opencode.json` below, which sets
  `0.6`. The SGLang engine samples at full speed.

> **ZML needs the 24 GB it asks for.** On 16 GB cards long prompts fail with an opaque
> `HTTP 500` — measured from ≥2,048 tokens on a 5080 and from ~700 on a 5060 Ti. Use the
> SGLang engine on 16 GB.

---

## Quickstart

Install the **[Escha runtime](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe)** first (wheel +
`serve.sh` + full detail, including two requirements that fail **quietly**) — then download this
model and serve it:

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -U pip wheel "huggingface_hub[cli]"

# torch MUST be pinned to 2.9.x. `escha._C` is ABI-linked to libtorch and the wheel does
# NOT declare a torch dependency, so a bare ">=2.9.0" resolves to 2.11 and `import escha`
# then fails with `undefined symbol: _ZN3c10...` — after two multi-GB downloads.
pip install "torch==2.9.*" --index-url https://download.pytorch.org/whl/cu128

# 1. runtime: fetch the sglang/ engine dir (wheel + serve.sh), install the wheel.
#    Use the glob — a pinned wheel filename goes stale on every rebuild.
hf download EschaLabs/escha-runtime-qwen3moe --include "sglang/*" --local-dir .
pip install ./sglang/escha-*.whl     # pulls transformers>=5.8 + the full dep closure

# 2. this model:
hf download EschaLabs/Qwen3.6-35B-A3B-Escha-W2 --local-dir ./escha-w2

MODEL=./escha-w2 bash sglang/serve.sh
```

Sanity-check the stack before serving — the first line must print three `True`s:

```bash
python -c "import torch, escha, sglang; print(torch.cuda.is_available(), hasattr(torch.ops.escha, 'escham_moe_linear'), bool(sglang.__version__))"
python -c "import escha; print(escha.__version__)"     # paste this into bug reports
```

Then:

```bash
curl -s http://127.0.0.1:30000/v1/models | python3 -m json.tool
```

> **If generation looks like fluent nonsense, check your `transformers` version first.**
> Below 5.8 the server does not fail — it logs one warning and then serves with the wrong
> architecture parameters. This is the single most likely cause of bad output.

---

## Connecting a client

The server speaks the standard OpenAI API, so anything that can point at a custom base URL works —
LM Studio, opencode, Open WebUI, the `openai` Python package, plain `curl`.

```
Base URL : http://127.0.0.1:30000/v1
Model    : escha-qwen36-35b-a3b-w2      (override with SERVED_NAME=...)
API key  : not required for localhost
```

`opencode.json` in this folder is a ready-made config for [opencode](https://opencode.ai) — copy it
to `~/.config/opencode/opencode.json`. It sets `temperature: 0.6` (Qwen's recommended sampling for
answer quality); on the **ZML** engine that halves decode speed — set `0` there if you want the
headline throughput instead.

If you expose the server beyond your own machine, set `HOST=0.0.0.0` **and** `API_KEY=...`, and put
it behind a VPN or tunnel rather than opening the port directly to the internet.

---

## Thinking mode

The model can reason before answering. Toggle it **per request** via `chat_template_kwargs` — a
top-level `enable_thinking` field is ignored:

```json
{
  "model": "escha-qwen36-35b-a3b-w2",
  "messages": [{"role": "user", "content": "..."}],
  "chat_template_kwargs": {"enable_thinking": true}
}
```

With thinking **on**, the reasoning arrives in `reasoning_content` and the answer in `content` —
read both. To turn thinking off for the whole server instead, start it with `THINK=0`.

`usage.reasoning_tokens` reports how much of the answer went to reasoning — use it to size a
[thinking budget](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/blob/main/sglang/INSTALL.md).

---

## Tuning

`serve.sh` documents every knob at the top of the file. The ones that matter most on a 24 GB card:

| Variable | Default | Notes |
|---|---|---|
| `MEM` | `0.78` | Fraction of VRAM reserved for the weight + KV pool. **Too low fails**, with "Not enough memory … increase --mem-fraction-static". Lower it only together with `CTXLEN`. |
| `CTXLEN` | `32768` | Context length. Raise once the defaults work. |
| `GRAPHS` | `1` | CUDA graphs — **mandatory for performance** on this launch-bound hybrid MoE (eager is ~4.4× slower). Set `0` only to debug a capture failure. |
| `RADIX` | `1` | Prefix caching. **`RADIX=0` is worth ~20% single-stream decode** here — the default is `1` for multi-turn agent reuse, so set it explicitly. See below. |
| `THINK` | `1` | `0` serves with thinking disabled by default. |
| `SERVED_NAME` | `escha-qwen36-35b-a3b-w2` | The model id clients must use. |

For per-architecture (incl. the RTX 50-series `ATTN_BACKEND=triton` knob) and per-VRAM
(16 / 24 / 40 GB+) launch recipes, see the **[runtime's "Running on your GPU" cookbook](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/blob/main/sglang/INSTALL.md)**.

---

## Verified configurations

Each command below was run on 2026-07-27 on the **first** card named in its heading, and produced
the numbers in [Performance across GPUs](#performance-across-gpus); a second name is a same-arch,
same-VRAM sibling the recipe should carry to, not a separately measured card. Copy the line for
your card. `MODEL=` and `VENV=` are omitted for brevity — set `MODEL` to your download directory.

**RTX 4090 / L40S — 24 GB, sm_89**

```bash
RADIX=0 MAXMAMBA=32 MAXREQ=32 CUDA_GRAPH_BS="1 2 4 8 16 32" \
  MEM=0.78 CTXLEN=32768 bash sglang/serve.sh          # 225 tok/s bs1 · 1,321 tok/s @ bs32
```

**RTX 3090 / A6000 — 24 GB, sm_86 (Ampere)**

```bash
RADIX=0 MAXMAMBA=16 MAXREQ=16 CUDA_GRAPH_BS="1 2 4 8 16" \
  MEM=0.78 CTXLEN=32768 bash sglang/serve.sh          # 154 tok/s bs1 · 390 tok/s @ bs16
# serving ≥8 concurrent streams? add INT8=off  (+12–20% aggregate, costs 2.2 GB of KV pool)
```

**RTX 5090 — 32 GB, sm_120**

```bash
# single user (best latency)
INT8=on ATTN_BACKEND=triton MEM=0.82 CTXLEN=32768 bash sglang/serve.sh    # 283 tok/s bs1
# batched (best throughput)
ATTN_BACKEND=triton MEM=0.82 CTXLEN=32768 MAXREQ=32 MAXMAMBA=48 RADIX=0 \
  CUDA_GRAPH_BS="1 2 4 8 16 32" bash sglang/serve.sh                      # ~2,670 tok/s @ bs32
```

**RTX 5080 / 5060 Ti — 16 GB, sm_120**

```bash
# many streams, short context — 16 concurrent 8k conversations
ATTN_BACKEND=triton MEM=0.92 CTXLEN=8192 CHUNK=2048 MAXREQ=16 MAXMAMBA=16 \
  RADIX=0 GRAPHS=1 CUDA_GRAPH_BS="1 2 4 8 16" bash sglang/serve.sh
# 5080: 212 tok/s bs1 · 914 tok/s @ bs16   |   5060 Ti: 128 tok/s bs1 · 387 tok/s @ bs16

# one stream, full context — the SAME pool spent on 32k instead of 16×8k
ATTN_BACKEND=triton MEM=0.92 CTXLEN=32768 CHUNK=2048 MAXREQ=2 MAXMAMBA=2 \
  RADIX=0 GRAPHS=1 CUDA_GRAPH_BS="1 2" bash sglang/serve.sh
```

**8k is the recipe's per-request cap, not the card's ceiling**[^ctxcap] — context and concurrency
draw on one shared KV pool, so a 16 GB card gives up one or the other, and which one is your call.

### Three settings that are worth getting right

- **`CUDA_GRAPH_BS` must list your maximum batch size.** If `MAXREQ=16` but the capture list
  stops at 8, batch 16 silently runs **eager** — measured **−8.8%** aggregate on a 5060 Ti, and it
  makes batch 16 look like a throughput ceiling when it is not. Costs ~2.5 s of startup and no
  VRAM.
- **`MEM=0.92`, not higher, on a 16 GB card.** At `0.94` a 16 GB card has ~0.43 GB of headroom and
  a `1024/1024` batch-16 request can OOM inside the fused MoE op and take the **whole server** down.
  `0.92` survives it and costs nothing in throughput.
- **`RADIX=0` unless you specifically need prefix caching.** On this hybrid model the radix cache
  is incompatible with the overlap scheduler, so `RADIX=1` silently disables it — worth **~20%
  single-stream decode** (measured 187 → 225 tok/s on a 4090) and it also clamps concurrency via
  the mamba state pool. Keep `RADIX=1` only for multi-turn agent workloads that genuinely reuse
  long prefixes.

This checkpoint is **text-only** (the `qwen3_5_moe` config declares a vision tower, but the quantized
weights contain none — vision is in the quant `ignore` list); `serve.sh` sets `SGLANG_VLM_TEXT_ONLY=1`
by default so the tower is never instantiated. Do not send image inputs.

---

## Requirements in detail

- **GPU** — **16 GB VRAM minimum** (fewer streams or less context, your choice[^ctxcap]; e.g. RTX 5060 Ti), **24 GB recommended**;
  NVIDIA Ampere (sm_80) through Blackwell (sm_120). The runtime ships a fat binary with native
  kernels for Ampere (sm_80/86), Ada (sm_89), Hopper (sm_90), and Blackwell (sm_100/sm_120), plus
  PTX for forward-compat on newer GPUs. The kernel launch route is auto-selected per GPU at runtime.
  Cards older than sm_80 (e.g. Turing) are not supported.
- **An NVIDIA driver — but no CUDA toolkit.** `ptxas` ships inside `triton`, which PyTorch already
  installs, and `serve.sh` probes that copy first; you do not need to install CUDA to serve this
  model. If discovery ever fails, point `TRITON_PTXAS_PATH` at a ptxas **binary** (not its
  directory — a directory is silently rejected).
- **Linux x86-64 with glibc ≥ 2.28** — the wheel is tagged `manylinux_2_28`, so Ubuntu 20.04+ and
  RHEL/Rocky/Alma 8+ are fine. WSL2 is untested.
- **`vm.overcommit_memory=1`** — on a fresh machine the first Triton compile forks a large process
  and fails under the default setting. `serve.sh` prints the one-line fix if it detects this.
- **`transformers >= 5.8` — ignore this file's `transformers_version` for pinning.** The runtime
  wheel installs a compatible transformers for you. Do **not** pin transformers to "match" any
  version field you find in the repo's `config.json` — versions below 5.8 lack this architecture's
  config class and serve fluent-looking nonsense with only a single warning.

### Format notes

- `escha_s_in` / `escha_s_out` ship as **all-ones**: the trained scales are already folded into
  `escha_rin` / `escha_rout` at export. Do not edit or "re-apply" them — non-ones values would be
  applied *on top of* the folded scales.
- `escha_config` (int32[9]) and `quantization_config.layer_meta` are **informational** (written by
  the exporter for offline tools). The runtime derives each projection's code rate from the code
  tensor's shape; `layer_meta` records it as `K` (2 for `gate_up_proj`, 3 for `down_proj`) with
  `bits` mirroring `K`.
- The `mtp.*` tensors (next-token-prediction head) are present in the checkpoint but **not
  served**; speculative decoding additionally needs a separate draft export that is not part of
  this release.

---

## Benchmarks

Two questions matter for a 2-bit build: **how much quality did it cost**, and **how does it serve**.
Quality is measured against an **FP8 baseline**[^fp8]; serving is measured on a **single RTX 4090**.

> **Which runtime produced these numbers.** Every figure on this page — quality and serving —
> was measured through the **SGLang engine** of the
> [escha-runtime-qwen3moe](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/tree/main/sglang)
> repo, using its shipped `serve.sh` and the launch recipes in
> [`sglang/INSTALL.md`](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/blob/main/sglang/INSTALL.md).
> The same repo also ships a **[ZML engine](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/tree/main/zml)**
> (single-binary, no Python) whose serving profile differs: higher sustained single-stream
> decode on long answers, but **one request at a time** — so none of the batched
> throughput or concurrency figures below apply to it. Pick the engine from the
> [runtime README](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe) comparison.

### Quality vs FP8

**Commonsense-6**[^cs6] — thinking-off, same box, paired:

| | GB | boolq | piqa | arc-e | arc-c | hellaswag | winogrande | **avg** |
|---|---|---|---|---|---|---|---|---|
| FP8 baseline | 35.0 | 84.46 | 82.59 | 71.93 | 54.86 | 83.38 | 73.40 | 75.10 |
| **this build** | **12.3** | **88.38** | **82.10** | **73.82** | **55.38** | **82.44** | **74.27** | **76.06** |

**Capabilities** — one representative benchmark per axis, this build vs the FP8 baseline. Retention is
this-build ÷ FP8.

| Capability | Benchmark | FP8 | **this build** | Δ | retention |
|---|---|---|---|---|---|
| Broad knowledge | MMLU-Pro (n=12,032) | 82.3 | **80.9** | −1.4 | 98.3% |
| Math reasoning | MATH-500 (n=500)[^math] | 91.2 | **93.8** | +2.6 | 102.9% |
| Graduate science | GPQA-Diamond (n=198)[^gpqa] | 74.7 | **77.8** | +3.1 | 104.2% |
| Coding | LiveCodeBench v6 (n=182)[^lcb] | 67.0 | **62.6** | −4.4 | 93.4% |
| Tool use | BFCL-AST, weighted (n=1000)[^bfcl] | 88.2 | **88.9** | +0.7 | 100.8% |
| Long context | RULER, 8k–128k avg[^ruler] | 89.4 | **89.9** | +0.5 | 100.5% |
| **mean**[^avg] | unweighted, 6 axes | **82.1** | **82.3** | **+0.2** | **100.2%** |

Across the six axes this 2-bit build stays within noise of the ~3× larger FP8 baseline everywhere except
long-horizon code generation (LiveCodeBench), the one capacity-bound gap. Coding parity is corroborated by
two better-powered paired-McNemar ties with FP8: HumanEval+ 92.07 vs 93.9 and CRUXEval-O 61.75 vs 63.0.[^code]

#### Evaluation protocol (reproduce these numbers)

Thinking mode and the token budget change reasoning scores materially, so both are stated per
benchmark. **Both arms (this build and FP8) always ran the identical protocol**, so every Δ above is
apples-to-apples.

| Benchmark | Thinking | Token budget | Notes |
|---|---|---|---|
| MMLU-Pro | **on**, 5-shot CoT chat | `max_tokens` **4,096** | **13.9% of answers hit the cap** (FP8: 13.0% — symmetric). See the caveat below. |
| MATH-500 | **on** + **thinking-budget cap** | budget 28,672 / `max_tokens` 32,768 | Cap forces `</think>` → **0 non-terminations**. |
| GPQA-Diamond | **on**, uncapped thinking | 16,384 | |
| LiveCodeBench v6 | **on** + thinking-budget cap | budget 16,384 / `max_tokens` 32,768 | |
| HumanEval+, MBPP+, CRUXEval-O | **off** | 4,096 | Thinking-on derails code extraction. |
| BFCL-AST, Commonsense-6 | **off** | 4,096 / loglikelihood | |
| RULER 8k–128k | **off** | retrieval | |

Sampling for the thinking-on runs is Qwen's recommended thinking config: `temperature=1.0,
top_p=0.95, top_k=20, min_p=0, presence_penalty=1.5`, n=1.

> **Caveat on the MMLU-Pro number (read if you are comparing to published leaderboards).** At a
> 4,096-token cap with thinking on, **13.9%** of questions run out of budget mid-reasoning; those are
> scored from the truncated trace and land at **49.5%** correct versus **86.0%** for answers that
> finish. FP8 truncates at the same rate (13.0%), so the **−1.4 gap is unaffected** — but both
> absolute numbers are **conservative by roughly 2–3 pp** against harnesses that allow a larger
> budget (this is the main reason our FP8 baseline reads 82.3 where Qwen publishes 85.2 for the
> unquantized model). If you re-run with a bigger budget — or better, with the
> [thinking-budget cap](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/blob/main/sglang/INSTALL.md#bounded-thinking-thinking_budget)
> that forces an answer — expect **both** arms to rise by a similar margin.

### KL divergence from BF16

The quality numbers above use an FP8 baseline because BF16 does not fit on a 24 GB card. This is
the direct measurement against the unquantized weights.

**0.0694 ± 0.0028 nats**[^kldbound] against `Qwen/Qwen3.6-35B-A3B` in BF16, over 524,032 held-out
positions.

| | |
|---|---|
| mean KL | **0.0694 ± 0.0028 nats** |
| top-1 agreement | 89.9% |
| median / p90 / p99 | 0.021 / 0.134 / 0.849 |
| wikitext2 / c4 / code | 0.088 / 0.052 / 0.068 |

What that means in practice: the 2-bit build picks the same next token as the full model **9 times
out of 10**, and where it differs it is usually a position the full model was unsure about anyway.
Give it text the full model finds ordinary and it is about **7% more surprised** by it. The full
model's own uncertainty on this corpus is 1.55 nats per token; quantization adds 0.069 on top of
that, roughly **4.5%**. This is at **5.6× compression**, 69.4 GB of BF16 down to 12.3 GB.

The per-position spread is wide (median 0.021, p99 0.849). Most tokens are unaffected; the
divergence concentrates on the 38.6% of positions where the full model's top choice is already
below 50%.

**Method.** Teacher-forced, batch size 1, no sampling. 256 sequences × 2048 tokens from held-out
splits of wikitext-2, C4 and codeparrot-clean-valid at pinned revisions; the exact token ids ship
as [`kld_corpus_v1.pt`](kld_corpus_v1.pt) (2.1 MB), so the corpus is reproducible without
`datasets`, network access, or those datasets continuing to exist. Both sides run under
`transformers`, so this is quantization error and not an inference-stack difference. Batch size is
part of the measurement: reduction order changes with batch composition, worth up to 0.75 on a
single logit between batch 1 and batch 4. The BF16 reference scored against its own cache reads
2.08e-08 nats.

### Performance across GPUs

Measured end-to-end on five consumer cards with the **SGLang engine**
([`sglang/`](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/tree/main/sglang); launch
recipes per card in the
[runtime cookbook](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/blob/main/sglang/INSTALL.md)).
*Decode = what one user sees streaming; peak throughput = total server output at the best batch size.*

| GPU | VRAM | arch | 1-user decode | TTFT (2k prompt) | peak server throughput | ctx in recipe[^ctxcap] |
|---|---|---|---|---|---|---|
| RTX 5090 | 32 GB | sm_120 | **283 tok/s**[^int8on] | 0.22 s | **~2,670 tok/s** @ bs 32 | 32k |
| RTX 4090 | 24 GB | sm_89 | **225 tok/s** | 0.26 s | **1,321 tok/s** @ bs 32 | 32k |
| RTX 5080 | 16 GB | sm_120 | **212 tok/s** | 0.18 s @1k | 914 tok/s @ bs 16 | 8k × 16 streams |
| RTX 3090 | 24 GB | sm_86 | **154 tok/s** | 0.63 s | 390 tok/s @ bs 16 | 32k |
| RTX 5060 Ti | 16 GB | sm_120 | **128 tok/s** | 0.52 s @1k | 387 tok/s @ bs 16 | 8k × 16 streams |

Every row was measured on that physical card with the launch command in
[Verified configurations](#verified-configurations) above — 2026-07-27, five independent
fresh-machine evaluations, one harness.

For scale: fast reading is ~5 words/s (≈7 tok/s) — even the slowest card here decodes ~18× faster
than you can read, and a 5090 serves a 32-user pool at interactive speed. Three levers matter on
every card: **CUDA graphs** (`GRAPHS=1`, the default — this hybrid MoE is launch-bound eager, graphs
are worth **4.4×**), **`RADIX=0`** for throughput/latency work (worth ~20% single-stream — see
Verified configurations), and the **`INT8` knob** (single-user vs batched).

Two things the spread above is *not*: it is not a VRAM ranking (the 16 GB 5080 beats the 24 GB
3090 by 38%), and it is not a generation ranking. It tracks **memory bandwidth and SM count** —
this is a 2-bit model, so decode is bandwidth-bound at batch 1 and compute-bound at batch.
Ampere (3090) is the slowest per stream and also the only card here where the kernel route
auto-selects `lovelace` rather than `blackwell`.

[^int8on]: 5090 and 3090 single-user numbers use `INT8=on` (int8-as-stored; measured +21–24% at
    bs 1 on the 5090, +35–42% on the 3090). Peak-throughput numbers use `INT8` off above 24 GB —
    int8 *costs* 11–52% at high batch, and the crossover is around **concurrency 8** (measured on
    the 3090). Cards ≤ 24 GB auto-enable int8; if you serve ≥ 8 concurrent streams on a 24 GB card,
    set `INT8=off` explicitly.

[^ctxcap]: **Every context figure on this page is the per-request cap in a shipped launch recipe, not
    a hardware limit.** Context costs KV, and KV is shared across concurrent requests, so a card spends one pool
    on either many short streams or few long ones. The 16 GB recipe is tuned for **16 concurrent 8k
    streams** out of a ~59k-token pool; lower `MAXREQ`/`MAXMAMBA` and the same card serves the
    model's **full 32k** window instead. Both 16 GB recipes, with their measured pool sizes, are in
    the [runtime cookbook](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe/blob/main/sglang/INSTALL.md).

### Serving — NVIDIA ISL/OSL grid, five GPUs

**Single-stream decode tok/s** by input/output shape, on the standard NVIDIA grid[^grid]. Five
independent fresh-machine evaluations, one card each, 2026-07-27. A dash means that evaluator did
not run that shape — the five chose overlapping but not identical grids, so the table is a union
rather than a full matrix[^gridconv].

| ISL / OSL | 5090 32 GB | 4090 24 GB | 5080 16 GB | 3090 24 GB | 5060 Ti 16 GB |
|---|---|---|---|---|---|
| 128 / 128 | **282.1** | **225.2** | **211.7** | **153.5** | **127.9** |
| 128 / 1024 | 275.9 | — | — | — | 126.5 |
| 128 / 2048 | — | 225.2 | 208.8 | 151.4 | — |
| 128 / 4096 | — | 224.0 | 201.1 | — | — |
| 500 / 2000 | — | 224.7 | 205.7 | — | — |
| 1000 / 1000 | — | 224.6 | 205.6 | — | — |
| 1000 / 2000 | — | 223.9 | 202.2 | — | — |
| 1024 / 128 | 270.6 | — | — | — | 125.1 |
| 1024 / 1024 | 266.2 | — | — | 148.0 | 124.0 |
| 1024 / 2048 | — | 223.9 | 202.1 | — | — |
| 2048 / 128 | 259.6 | 221.2 | 198.9 | 145.7 | — |
| 2048 / 2048 | 251.8 | 222.5 | 196.5 | 148.6 | — |
| 4096 / 128 | — | — | — | — | 117.4 |
| 4096 / 1024 | — | — | — | — | 116.5 |
| 5000 / 500 | — | 219.4 | 185.8 | — | — |
| 20000 / 2000 | — | 202.7 | — | — | — |

**Single-stream decode barely moves with prompt length.** From a 128-token prompt to a 2,048-token
one it falls 11% on the 5090, 2% on the 4090, 7% on the 5080, 5% on the 3090; the 4090 still holds
90% of its short-prompt rate at a 20,000-token prompt. Decode is bandwidth-bound and the KV read
is small next to the weights, so what you pay for a long prompt is TTFT, not tokens per second.

Under concurrency each card's peak, with the shape and recipe that produced it:

| GPU | peak aggregate | at | recipe |
|---|---|---|---|
| RTX 5090 | **3,017.6 tok/s** | 128/1024, 32 streams | batched, `INT8` off |
| RTX 4090 | **1,321 tok/s** | 128/128, 32 streams | batched, `INT8` off |
| RTX 5080 | **914.1 tok/s** | 128/128, 16 streams | 16 GB recipe |
| RTX 3090 | **389.7 tok/s** | 128/2048, 16 streams | `INT8` on |
| RTX 5060 Ti | **387.1 tok/s** | 128/1024, 16 streams | `INT8` off |

The 4090 grid was also **reproduced from scratch on a second 4090** following only these public
docs: every bs-1 shape matched within 0.1–1.8%, including the 20,000-token cell to 0.1%.

### Latency SLA — MLPerf-style Poisson arrivals, RTX 4090

Poisson arrivals[^sla] — 1000-in / 400-out, 100 requests per point, nearest-rank p99:

| arrival rate | TTFT p50 | TTFT p99 | TPOT p99 | out tok/s | Interactive | Conversational |
|---|---|---|---|---|---|---|
| **1.0 req/s** | 168 ms | **433 ms** | 16.3 ms | 445 | **PASS** | **PASS** |
| 1.25 req/s | 197 ms | 1,073 ms | 20.6 ms | 550 | fail | **PASS** |
| 1.5 req/s | 304 ms | 3,281 ms | 20.6 ms | 640 | fail | fail |
| 2.0 req/s | 5,947 ms | 8,001 ms | 20.5 ms | 717 | fail | fail |
| 12.0 req/s | 21,454 ms | 41,964 ms | 19.8 ms | 772 | fail | fail |

Saturation is **~1.9 req/s** (772 tok/s ÷ 400 output tokens). Past that, waits grow by ordinary
queueing, not by any defect. **Decode is never the limiter** — TPOT keeps 2.4–45× headroom at every
rate tested; the binding constraint is always TTFT/prefill[^tpot].

[^kldbound]: Lower bound. Storing the full distribution over 524k positions × 248,320 vocabulary
    would take ~500 GB, so the reference keeps its top-1024 tokens plus a residual bucket.
    Coarsening cannot increase KL, so the figure can only understate. Measured on this pair:
    K=1024 recovers 98.45% of the K=32768 value (K=512 97.52%, K=2048 99.08%, K=8192 99.76%),
    putting the resolved value at ≈0.0705 nats. Only 0.93% of the BF16 model's probability mass
    falls outside its top 1024 tokens.

[^fp8]: FP8 is the baseline because it is the closest widely-available reference to full precision
    (it tracks BF16 on these tasks), and because BF16 for this model does not fit on a 24 GB card at
    all. FP8 itself needs ~35 GB, so the comparison is against a build that requires substantially
    more hardware than this one. The KL section does measure against BF16 directly; that pass
    streams the weights from disk a layer at a time, which is fine for scoring a fixed corpus once
    but far too slow to serve.

[^cs6]: Same box, same in-process harness for both arms, so backend differences cancel. The
    dense (non-expert) layers here are int8; that is **lossless** against an fp16-dense build of the
    same weights (boolq 88.38 vs 88.04), so the size saving costs nothing measurable.

[^math]: MATH-500 is served with a thinking-budget cap — the correct protocol for a reasoning model
    (0 non-terminations; uncapped, the model over-thinks and truncates, which the cap fixes without
    changing answer quality). Read the result as **parity** with FP8; the small margin is capping
    protocol, not a real quality gain.

[^gpqa]: GPQA-Diamond is run-to-run unstable by ±~5 pp at this sample size, so treat +3.1 as an
    **effective tie** with FP8, not a genuine lead.

[^lcb]: LiveCodeBench v6, `release_v6` slice (contest dates 2025-01 onward, N=182) — a
    post-training-cutoff subset chosen to limit contamination. Both builds are scored on the same
    182 problems, so read −4.4 as **retention vs FP8**, not a leaderboard score. Long-horizon code
    generation is the most capacity-sensitive task measured, and the one clear 2-bit gap.

[^bfcl]: BFCL-AST, matched same-driver run (thinking-off, n=1000, AST-weighted across the four
    non-live categories). Tool-call form is preserved at 2-bit — a tie with FP8.

[^ruler]: RULER (synthetic long-context retrieval), 4-task average across 8k / 32k / 64k / 128k.
    Near-lossless through 128k.

[^avg]: **Unweighted** mean of the six rows — a reading convenience, not a statistic to lean
    on. The axes have wildly different sample sizes (MMLU-Pro n=12,032 vs LiveCodeBench
    n=182) and different score scales, so the mean hides the one real gap (coding) behind
    gains elsewhere. Read the per-axis rows for anything that matters.

[^code]: Paired McNemar (exact two-sided) on identical prompts — per-item comparisons on full native
    sample sets. Both land on a statistical tie: HumanEval+ turns on just 7 disagreements (2 win /
    5 loss of 164 — underpowered), CRUXEval-O is far better powered (64 disagreements) and still ties.

[^grid]: Measured with CUDA graphs on and a 16-request cap (`GRAPHS=1 MAXREQ=16`), prefix caching
    **off** (`RADIX=0`), and output length pinned so every cell decodes the full OSL. `GRAPHS=1`
    and `RADIX=0` are both required to reproduce these numbers; `GRAPHS=1` is already the
    `serve.sh` default, `RADIX=0` is not. Single-stream (bs 1) is flat at ~220 tok/s across shapes
    because decode is memory-bound, not compute-bound, at batch 1.

[^gridconv]: The five evaluators used their own harnesses, so the **single-stream** column is the one
    metric all five report identically (per-stream decode rate, equivalently `1000 / TPOT`); it is
    quoted as measured, never derived. Their aggregate-throughput conventions do *not* match — two
    report a decode-window rate and three an end-to-end rate that amortizes prefill and batch ramp —
    which is why concurrency appears as each card's own peak with its recipe, rather than as extra
    columns here. Two caveats those peaks inherit: **short-output cells at batch understate steady
    decode**, because with only 128–500 output tokens the ramp in and out of the batch is a large
    share of wall time; and at very long inputs the KV pool cannot hold 16 concurrent requests, so
    some queue and the figure is pessimistic rather than a tuning miss.

[^sla]: MLPerf Server-style: Poisson arrivals (not synchronized bursts) and p99 rather than median —
    burst harnesses systematically misreport this workload. Thresholds are the MLPerf interactive
    categories: **Interactive** = TTFT p99 ≤ 450 ms and TPOT ≤ 40 ms; **Conversational** = ≤ 2000 ms
    and ≤ 200 ms.

[^tpot]: One caveat worth knowing before you turn thinking on: TTFT measures the first token
    *generated*, but with thinking enabled the first token a **user sees** comes after the reasoning
    block. On real problems that gap is large — first generated token in ~75 ms, first answer token
    at a median of ~15 s, and a long tail. Capping the thinking budget removes the runaway tail. If
    latency to a visible answer matters more than reasoning depth, serve with `THINK=0`.

### Apple Silicon (MLX)

The same weights run on macOS through **[escha-mlx](https://github.com/EschaLabs/escha-mlx)**, a
separate MLX runtime with continuous batching, prefix caching and an OpenAI-compatible endpoint. It
loads this repo directly, with no conversion step.

| | M4 base | M4 Pro 48 GB | M5 Pro |
|---|---|---|---|
| resident memory | 12.25 GB | 12.25 GB | 12.25 GB |
| prefill, 512 tok | 264 tok/s | 263.8 tok/s | **756.5 tok/s** |
| decode, single stream | 27.3 tok/s | 41.3 tok/s | **59.7 tok/s** |
| batch 8, aggregate | 59.6 tok/s | 104.7 tok/s | 193.0 tok/s |
| batch 16, aggregate | 104.0 tok/s | 179.6 tok/s | 240.0 tok/s |
| batch 128, aggregate | 185.6 tok/s | | **539.3 tok/s** |

**These are not comparable to the NVIDIA numbers above.** An M4 base moves ~120 GB/s where a 4090
moves 1008 GB/s. Decode on this model is memory-bound, so the gap is the machine, not the runtime.

Requirements: Apple Silicon M1–M5, macOS 14+, Python 3.10–3.13, **24 GB unified memory**.

**Why 2-bit on a Mac.** A stock MLX 4-bit build of this model is 19.51 GB against 12.25 GB here. On
a 24 GB Mac the 4-bit build is **faster for a single stream** (42.9 vs 27.3 tok/s), but it exhausts
memory at batch 16, where this build sustains 104 tok/s. Take 4-bit if you run one conversation at
a time and have the headroom; take this one if you need concurrency, long context, or the rest of
your machine back.

## Licenses and attribution

This repository contains **model weights only**, released under the **Apache License, Version 2.0**
(see [`LICENSE`](LICENSE)).

- **Model weights** — a 2-bit quantized derivative of Qwen3.6-35B-A3B (Apache-2.0, Qwen); base
  license text at [`THIRD_PARTY_LICENSES/Qwen-LICENSE.txt`](THIRD_PARTY_LICENSES/Qwen-LICENSE.txt).
- **Tokenizer** — Qwen (`Qwen2Tokenizer`), Apache-2.0.
- **Chat template** — from
  [froggeric/Qwen-Fixed-Chat-Templates](https://huggingface.co/froggeric/Qwen-Fixed-Chat-Templates)
  (Apache-2.0, inherited from Qwen), which fixes tool-calling and thinking-mode handling for
  this model family.

The **runtime** (the `escha` wheel: the SGLang serving fork + CUDA kernels, and their third-party
licenses — SGLang, exllamav3, AQLM, and the BSD-3/MIT upstreams vendored in SGLang) is distributed
separately and carries its own `LICENSE` + `THIRD_PARTY_LICENSES/`:
**[EschaLabs/escha-runtime-qwen3moe](https://huggingface.co/EschaLabs/escha-runtime-qwen3moe)**. All bundled code there is permissive
(Apache-2.0 / MIT / BSD-3-Clause) — no copyleft.
