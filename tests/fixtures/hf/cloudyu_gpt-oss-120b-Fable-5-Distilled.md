---
base_model: gpt-oss-120b-heretic-v2-mxfp4-q8-hi-mlx
tags:
  - mlx
  - lora
  - muon
  - apple-silicon
  - moe
  - coding
  - agent
  - fine-tuned
language:
  - en
datasets:
  - armand0e/claude-fable-5-claude-code
---

# gpt-oss-120b-Fable-5-Distilled

**A LoRA fine-tuned MoE coding agent model distilled from real-world Claude Code programming sessions. Merged into a single complete model — download and run directly on Apple Silicon via MLX.**

> **Recommended temperature: `0.95`** — this model was trained on opencode agent traces where the assistant alternates between reasoning, tool calls, and code generation. Slightly higher temperature preserves this multi-modal behavior.

**GGUF format is ready ([autotrust/gpt-oss-120b-Fable-5-Distilled-GGUF](https://huggingface.co/autotrust/gpt-oss-120b-Fable-5-Distilled-GGUF))
---

## Test Results (HumanEval PASS@1)

| Model | Quant | Score | Pass/Fail |
|-------|-------|-------|-----------|
| Fable-5-Distilled | **Q5_0** (67 GB) | **99.39%** | 163/164 |
| Fable-5-Distilled | **Q8_0** (115 GB) | **98.78%** | 162/164 |
| gpt-oss-120b (base) | MXFP4 | 83.54% | 137/164 |

# Test Details([cloudyu/gpt-oss-120b-Fable-5-Distilled-GGUF](https://huggingface.co/cloudyu/gpt-oss-120b-Fable-5-Distilled-GGUF))

## Model Summary

`gpt-oss-120b-Fable-5-Distilled` is a **fully merged LoRA fine-tune** of `gpt-oss-120b-heretic-v2-mxfp4-q8-hi-mlx`, trained using the **Muon optimizer** with Newton-Schulz orthogonalization on Apple MLX. The fine-tuning data consists of 352 real-world opencode programming sessions extracted from `armand0e/claude-fable-5-claude-code`.

This is a **complete model upload** — no separate adapter files or base model are needed.

The model learns to act as a coding agent: understanding user requests, exploring repositories, making code edits via tool calls, and delivering final solutions — all through the Harmony channel protocol (`analysis` for internal reasoning, `final` for the delivered response).

---

## Highlights

- **🔧 Agent-style coding** — trained on real tool_use traces (Bash, Read, Edit, TaskCreate, Git) from Claude Code sessions. Generates natural tool-call sequences.
- **🧠 Muon optimizer** — Newton-Schulz orthogonalized updates on LoRA matrices for stronger convergence at low training step counts.
- **🎯 13/13 PASS** — perfect score on a 13-task custom benchmark spanning math olympiad, algorithm coding, DS/algo, logic puzzles, and scientific computing.
- **🌡️ Recommended temperature: `0.95`** — preserves the agent's multi-step reasoning + tool-call rhythm.
- **🍎 Fully on-device** — no cloud API, no GPU cluster. Pure MLX inference on Mac.
- **📦 Full model** — merged weights included. No adapter setup required.
- **📐 Harmony channel format** — `analysis` (chain-of-thought) and `final` (response) channel separation.

---
## Tool Call details
See **[TOOL_CALLING.md](TOOL_CALLING.md)** for the full tool calling guide.

## Quick Start

### macOS + MLX

```bash
# Using mlx_lm (installed by default with mlx)
mlx_lm.chat --model gpt-oss-120b-Fable-5-Distilled --max-tokens 10000 --temp 0.95
```

### Python

```python
from mlx_tune import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="gpt-oss-120b-Fable-5-Distilled",
    max_seq_length=4096,
    load_in_4bit=True,
)

prompt = """<|start|>system<|message|>You are a helpful coding assistant.
Reasoning: high
# Valid channels: analysis, commentary, final<|end|>
<|start|>user<|message|>Write a function to find the longest common substring of two strings.<|end|>
<|start|>assistant<|channel|>analysis<|message|>"""

outputs = model.generate(prompt, max_new_tokens=2048, temperature=0.95, top_p=0.9)
print(outputs)
```

### Prompt Format (Harmony)

This model uses the `gpt-oss` Harmony channel protocol:

```
<|start|>system<|message|>{system prompt}
Reasoning: high
# Valid channels: analysis, commentary, final<|end|>
<|start|>user<|message|>{your request — including coding tasks, tool-call requests, etc.}<|end|>
<|start|>assistant<|channel|>analysis<|message|>{internal chain-of-thought}<|end|>
<|start|>assistant<|channel|>final<|message|>{final answer / tool call sequence}<|return|>
```

- The `analysis` channel contains the model's internal reasoning. Display or hide depending on use case.
- The `final` channel contains the deliverable response (code, tool calls, or natural language).
- Always prompt the model to begin with `<|start|>assistant<|channel|>analysis<|message|>`.

---

## Training Details

| Parameter | Value |
|---|---|
| Base model | `gpt-oss-120b-heretic-v2-mxfp4-q8-hi-mlx` |
| Architecture | MoE (Mixture of Experts), 120B params, top-k=4, 128 experts |
| Quantization | mxfp4 weights + q8 hi-precision activations |
| Framework | Apple MLX + mlx-tune |
| Optimizer | **Muon** — Newton-Schulz orthogonalized momentum (ndim >= 2) + AdamW fallback (1-D params) |
| LoRA rank / alpha | r=16, α=32 |
| LoRA dropout | 0.0 |
| LoRA target modules | q/k/v/o/gate/up/down projections + router (SwitchLinear expert layers) |
| Router treatment | LoRA on router (top-k=4 — sufficient competition, no special unfreezing needed) |
| Muon learning rate | 1e-5 |
| AdamW learning rate | 1e-5 |
| Muon momentum | 0.95 |
| Newton-Schulz steps | 5 |
| Effective batch size | 2 × grad accum 8 = 16 |
| Training steps | 40 |
| Warmup ratio | 0.05 |
| LR scheduler | Cosine decay |
| Max sequence length | 4096 tokens |
| Peak memory during training | ~110 GB unified memory |
| Training hardware | Apple Silicon M-series (>= 64 GB recommended) |

### Dataset

- **Source:** [`armand0e/claude-fable-5-claude-code`](https://huggingface.co/datasets/armand0e/claude-fable-5-claude-code)
- **Type:** Opencode session logs — real-world Claude Code programming agent traces
- **Extracted samples:** 352 user → assistant turns (from 55 session files, ~100 sessions)
- **Content:** tool_use sequences (Bash, Read, Edit, TaskCreate, Git), code generation, multi-step agent workflows
- **Format:** Converted from opencode event format → Harmony channel protocol
- **Split:** 90% train (317) / 10% validation (35), seed=42

### Muon Optimizer

Muon provides faster convergence than AdamW for matrix-shaped parameters by orthogonalizing gradient updates via Newton-Schulz iteration:

- **Matrix params (ndim >= 2):** LoRA A/B matrices → Muon (Nesterov momentum + NS orthogonalization + shape-aware scaling)
- **1-D params / bias:** → AdamW fallback

Unlike our previous BAdam-based models, this release uses uniform Muon training across all LoRA layers, including the router. At top-k=4, the router competition space is sufficient to avoid expert collapse without special lr treatment.

---

## Benchmark Results

Custom hard benchmark — 13 tasks across math, coding, logic, and science. Auto-graded with keyword matching + live code execution (60s timeout per task, max 2 retries on error).

| ID | Task | Verdict | KW% | Time | Tok/s |
|---|---|---|---|---|---|
| math_02 | Euler Totient Sum — last 6 digits | ✅ PASS | 100% | 41.9s | 13 |
| math_03 | Lattice Paths Avoiding the Anti-Diagonal | ✅ PASS | 100% | 98.2s | 16 |
| math_04 | Segmented Sieve in [10¹², 10¹²+10⁶] | ✅ PASS | 100% | 71.8s | 15 |
| code_01 | Median of Two Sorted Arrays | ✅ PASS | 100% | 62.7s | 14 |
| code_02 | Thread-Safe LRU Cache with TTL | ✅ PASS | 100% | 114.7s | 14 |
| code_03 | Persistent Segment Tree — K-th Query | ✅ PASS | 100% | 194.7s | 16 |
| code_04 | Multi-Head Attention + RoPE (NumPy) | ✅ PASS | 100% | 114.3s | 13 |
| code_05 | Dijkstra vs A* on Geometric Graph | ✅ PASS | 100% | 119.1s | 13 |
| logic_01 | Knights & Knaves — Exhaustive SAT | ✅ PASS | 100% | 41.7s | 15 |
| logic_02 | Verify Three Mathematical Claims | ✅ PASS | 100% | 47.2s | 14 |
| sci_01 | Figure-8 Three-Body Orbit — Energy Conservation | ✅ PASS | 100% | 101.9s | 14 |
| sci_02 | Metropolis-Hastings vs HMC Comparison | ✅ PASS | 100% | 110.5s | 13 |
| sci_03 | Optimizer Comparison on Rosenbrock | ✅ PASS | 100% | 70.4s | 12 |

**Overall: 13/13 PASS  |  Avg KW: 100.0%  |  Total benchmark time: 1189s**

All 13 tasks pass on the first attempt, zero retries required. The model consistently generates correct, executable code with full keyword coverage.

### Key Benchmark Details

- **code_01** Median — O(log n) binary search vs merge: **5656× speedup**, correct.
- **code_02** LRU Cache — 8-thread stress test: **710k ops/sec**, hit_rate 49.8%, 200k evictions.
- **code_03** Persistent Segment Tree — Q1=3, Q2=2, Q3=31, Q4=1 all correct.
- **code_04** Multi-Head Attention + RoPE — causal mask verified, max_future_attn = 0.0.
- **sci_01** Three-body — energy drift only **3.0e-14**, numerical precision excellent.
- **sci_02** HMC — ESS 379k (MH: 1,930), gradient direction correct (p += grad_log_target).

### Inference Speed

| Platform | Throughput |
|---|---|
| Apple Silicon M-series (MLX, 4-bit) | **12–16 tok/s** |
| Peak memory (inference) | ~69 GB |

This is a 120B MoE model running entirely on-device on a Mac — no cloud dependency, no quantization compromise.

---

## Limitations

- **Apple Silicon only** — quantized and optimized for MLX. Not compatible with CUDA/ROCm without re-quantization.
- **GGUF format is ready, Now can run anywhere ([autotrust/gpt-oss-120b-Fable-5-Distilled-GGUF](https://huggingface.co/autotrust/gpt-oss-120b-Fable-5-Distilled-GGUF))
- **40-step checkpoint** — an early fine-tune designed for quick validation. Further training would deepen the coding agent behavior.
- **No RLHF** — trained on supervised opencode session data only. Safety alignment is lighter than commercial instruction-tuned models.
- **Harmony prompt format required** — this model expects the `<|channel|>` protocol. Standard ChatML or Alpaca-style prompts will produce degraded results.
- **Small dataset** — 352 turns is modest. The benchmark results suggest high-quality, high-signal data, but broader generalization benefits from more training data.

---

## Citation / Acknowledgements

- Base model: `gpt-oss-120b-heretic-v2`
- Training dataset: [`armand0e/claude-fable-5-claude-code`](https://huggingface.co/datasets/armand0e/claude-fable-5-claude-code)
- Optimizer: Muon — [Muon: An optimizer for hidden layers in neural networks](https://github.com/KellerJordan/Muon)
- Framework: [Apple MLX](https://github.com/ml-explore/mlx) · [mlx-tune](https://github.com/unslothai/unsloth-mlx)
- Agent traces from: Claude Code (Anthropic) via opencode session logs
