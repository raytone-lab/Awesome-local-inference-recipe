---
library_name: transformers
base_model:
- Jackrong/Qwopus3.8-27B-Flash
tags:
- image-text-to-text
- vision
- multimodal
- text-generation-inference
- transformers
- unsloth
- conversational
- text-generation
- qwen3_5
- qwen3
- qwen
- 27b
- fine-tuned
- instruction-tuned
- reasoning
- agent
- agentic
- tool-use
- function-calling
- code-generation
- mtp
- speculative-decoding
- local-inference
- safetensors
license: apache-2.0
language:
- en
- zh
- es
- ru
- ja
pipeline_tag: image-text-to-text
base_model_relation: finetune
---
# 🪐 Qwopus3.8-27B-Flash-V2

<div align="center">
  <img src="https://cdn-uploads.huggingface.co/production/uploads/66309bd090589b7c65950665/UBRjhjok17Kvz-NA03VoD.jpeg" alt="IMG_7359" width="82%"/>
</div>

> [!NOTE]
> **Qwopus3.8-27B-Flash-V2** is a renewed post-training release of [Qwopus3.8-27B-Flash](https://huggingface.co/Jackrong/Qwopus3.8-27B-Flash), whose foundation is [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B).

> [!TIP]
> **Revised Rewards and Reinforcement Learning · Improved Python Formatting**

## 💡 1. Fine-Tuning Philosophy — Preserve Capability, Collapse Cost

Qwopus3.8-27B-Flash-V2 is a renewed post-training release of [Qwopus3.8-27B-Flash](https://huggingface.co/Jackrong/Qwopus3.8-27B-Flash), which itself is built on [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B). The goal remains the same: preserve enough capability for demanding work while reducing ineffective reasoning and making long-running agent workloads more practical.

An agent amplifies reasoning cost. A normal chat may call a model once, but one agent task can call it dozens or hundreds of times through a repeated loop:

```text
Read → Think → Tool Call → Observe → Edit → Test
```

> [!IMPORTANT]
> **Wall-clock time is what users feel.** If a model adds five seconds to each turn, a 50-turn task adds 250 seconds of waiting. In the agent era, every-token speed, reasoning length, and completion efficiency are as important as a single-turn benchmark result.

Inference cost is also a central commercialization constraint. Every generated token consumes GPU time, electricity, memory capacity, and concurrency budget. Flash models are intended to give users with constrained resources a more practical experience, not merely to produce a higher throughput number on paper.

V2 keeps this efficiency-oriented philosophy while applying another round of post-training to the Flash model. It uses different reward functions and reinforcement-learning methods from the earlier Flash training run.

The objective is to reduce ineffective computation and reach a clean completion more quickly and consistently. Efficiency remains an explicit trade-off: a shorter reasoning trace is useful only when the model still completes the task correctly. The benchmark sections below report the measured scope of that trade-off.


### Five-Story Pagoda Garden — Visual Output Comparison

> [!NOTE]
> These visuals are qualitative model outputs. They complement the measured benchmark results below and are not a quantitative capability score on their own.

#### Original Base Model — Qwen3.8-27B

![Original model — Five-Story Pagoda test](https://cdn-uploads.huggingface.co/production/uploads/66309bd090589b7c65950665/r2jq2T2BEdtQJMYCMaMzR.png)

#### Fine-Tuned Model — Qwopus3.8-27B-Flash-V2

![Fine-tuned model — Five-Story Pagoda test](https://cdn-uploads.huggingface.co/production/uploads/66309bd090589b7c65950665/7YGeM1vEeJgS7wDXcz3eq.png)


## 🧪 2. Fine-Tuning Cookbook

### 2.1 Base Model and Training Lineage

Qwopus3.8-27B-Flash-V2 is post-trained from **Qwopus3.8-27B-Flash**, with Qwen3.8-27B as the original foundation model. The V2 run inherits the earlier release's SFT and reasoning-reinforcement pipeline as its starting point, then applies a new post-training pass with different rewards and reinforcement-learning methods.

The training objective is not simply to maximize visible reasoning length or claim a universal benchmark gain. It is to retain practical problem-solving ability while making the model faster, less prone to pathological long-tail reasoning, and better suited to iterative agent workflows.

### 2.2 Stage 1 — Inherited Data Preparation and Quality SFT

The inherited SFT stage began with approximately **1.5 million** teacher-model examples. After extensive cleaning and filtering, the highest-quality **10%** was retained for the initial fine-tuning stage.

Each example was evaluated across its three main components—**question**, **chain of thought**, and **answer**—with criteria tailored to a 27B model:

- Semantic relevance and usefulness.
- Problem difficulty.
- Chain-of-thought quality.
- Answer consistency.

The evaluation ensemble used reasoning models including **Qwen3.7-Max**, **GLM-5**, **GPT-OSS-120B-High**, and **Gemma4-27B**. Their scores were combined through a weighted calculation, after which only high-quality examples were retained.

> [!NOTE]
> The inherited training mix also includes agent-trajectory data and reconstructed trace data derived from closed models such as Claude and GPT.

### 2.3 Stage 2 — Inherited Reasoning Reinforcement

The inherited pipeline also included a reasoning-reinforcement stage that consolidated and strengthened the chain-of-thought and reasoning behaviors learned during SFT. The earlier Flash card describes that inherited stage as **NVIDIA NeMo-RL + GSPO**. V2 retains that inherited foundation and then applies a revised post-training pass with different reward functions and reinforcement-learning methods; the exact V2 recipe is not disclosed here. The intent was to reinforce useful reasoning trajectories and completion behavior rather than reward longer reasoning traces by default.

> [!TIP]
> The stages serve different roles: the inherited SFT builds a high-quality reasoning and instruction-following foundation; inherited and V2 reinforcement stages consolidate that foundation through reward-guided reasoning reinforcement.

### 2.4 Python Indentation — Working Hypothesis

V2 was developed in response to the Python indentation issue reported for the earlier Flash release. In the reported tests, the issue is substantially reduced under the recommended coding configuration, but the mechanism below remains a **working hypothesis**, not a proven causal account.

One plausible pathway is that part of the training mix contained reconstructed reasoning traces derived from Claude/GPT-style reasoning-chain attack-reversal data. Some Python drafts generated within those reconstructed reasoning traces may have contained invalid indentation or otherwise malformed formatting. If a Python monitor or verifier did not reliably reject every malformed draft, those outputs could still receive reward. Subsequent reasoning reinforcement could then amplify the formatting pattern because the reward signal treated it as successful. This hypothesis is consistent with a failure mode in which a formatting defect is reinforced by an incomplete measurement signal, but it does not establish exactly which data examples or verifier behavior caused the original issue.

The available evidence is local and configuration-dependent. In the local temperature-**0.3** Python-formatting check, no formatting failures were observed. This is encouraging evidence for the recommended setting, not a universal guarantee that all Python generations will be correctly indented.

### 2.5 Recommended Coding Parameters — xhigh with `temperature=0.3`

For coding and agentic software-engineering tasks, especially Python, start with **xhigh reasoning and an explicit `temperature=0.3` override**. The V2 Hugging Face `generation_config.json` still lists `temperature=1.0`, so the lower temperature must be supplied by the caller; it is not the repository default.

Pass the reasoning controls to the chat template and the sampling temperature to generation explicitly:

| Setting | Value | Where to apply it |
| --- | --- | --- |
| `enable_thinking` | `True` | Chat-template arguments |
| `reasoning_effort` | `"xhigh"` | Chat-template arguments |
| `temperature` | `0.3` | Generation / sampling arguments |

Keep the remaining sampling settings from the model's actual runtime configuration unless you have a separate reason to tune them. In particular, the repository generation configuration uses `top_p=0.95` and `top_k=20`; this recommendation changes the temperature, not those other values.

Kyle's reported local comparison was:

| xhigh coding setting | Average thinking characters per task | Relative comparison |
| --- | ---: | --- |
| `temperature=0.3` | **4,357** | About **13.2% shorter** than 0.7 |
| `temperature=0.7` | **5,017** | Reference |

In the local temperature-**0.3** Python-formatting check, no formatting failures were observed. A Fisher exact test comparing the 0.3 and 1.0 conditions reported **p = 0.00267** for the null hypothesis that their indentation-failure rates are equal. This p-value is the probability, under that null hypothesis, of observing the measured result or a more extreme result; it is not the probability that the null hypothesis is true. The reported p-value is reproduced as provided; because the raw 2×2 contingency table is not included here, it was not independently recomputed. The test does not provide a universal failure rate and should not be interpreted as a guarantee for every prompt or environment.

## 🙏 3. Training Stack, Testing, and Collaboration

### Unsloth

Special thanks to [Unsloth](https://unsloth.ai/) for its efficient, memory-optimized fine-tuning framework. Its tooling made the large-model training workflow more practical and accessible.

### Kyle Hessling

Special thanks to [**Kyle Hessling**](https://x.com/KyleHessling1) for completing the testing work and providing essential evaluation support for this release, including the coding-configuration comparison and Python-formatting check described above.

> [!TIP]
> If you have any questions or suggestions about the model, please feel free to reach out to [Kyle Hessling](https://x.com/KyleHessling1) on [X](https://x.com/KyleHessling1) and share your feedback. Thank you so much for all your support! 🙏

> [!NOTE]
> The training and test results in this card are author-provided local results. The sections below describe the measured scope and do not claim universal behavior across all hardware, prompts, sampling settings, or agent environments.

## 📊 4. Benchmark Results

The summary below combines the final V2 accuracy with the Qwopus-Flash and Qwen base results. The reported MMLU-Pro result was measured under a **64K context** with the **official recommended thinking-mode configuration**. Different runs used different quantization and reasoning settings, so the scores, speeds, and acceptance rates are not a controlled cross-version comparison.

### 4.1 Benchmark Summary

| Reported signal | V2 | Qwopus-Flash | Qwen3.8 base |
| --- | ---: | ---: | ---: |
| MMLU-Pro accuracy | **92.33%** | 91.28% | **92.73%** |
| Decoder-only throughput | — | **9.347 tok/s** | 8.284 tok/s |
| Weighted MTP draft acceptance | — | **80.7%** | 66.1% |
| Aggregate `raw_output` characters | — | **7,949,546** | 8,824,213 |
| End-to-end batch evaluation throughput | — | **~8% higher** | — |
| Agentic software-engineering battery | **14 / 14 (100%)** | **14 / 14 (100%)** | — |

### 4.2 Evaluation Scope

The reported local tests used multiple NVIDIA hardware configurations. The current test brief does not map every table or case study to a particular device.

For the Qwopus-Flash/Qwen3.8 base MMLU-Pro decoder-only comparison, both models used the same Q5_K_M + MTP configuration:

```text
draft_n_max = 2
-c 327680
-np 10
```

The Qwopus-Flash agentic software-engineering run in Section 4.3 was explicitly reported on one RTX 5090. Its recorded timings and configuration remain attributed to that run.

**MMLU-Pro configuration:** The reported result was measured under a **64K context** with the **official recommended thinking-mode configuration**. This result is separate from the local temperature-0.3 Python-formatting study.


### 4.3 Agentic Software-Engineering Battery

> [!TIP]
> **Qwopus-Flash result: 14 / 14 tasks passed (100%), as reported by the release author.** The task battery and pass criteria below are retained. All fourteen tasks, including T07, passed. Per-task timings, turns, throughput, and repeated-seed measurements were not supplied; the detailed measurements below use the Qwopus-Flash run.


This held-out battery evaluates **14 agentic software-engineering tasks** with deterministic hidden-test verifiers. There is no LLM-as-judge and no partial credit: a task passes only when its complete hidden suite passes. Before evaluation, every task was checked with negative and positive controls—the untouched starting state had to fail, and a reference solution had to pass. Hidden tests remain outside the agent workspace and are SHA-256 hashed before and after each run to detect tampering.

> [!IMPORTANT]
> **Qwopus-Flash comparison result: 14 / 14 passed (100%).** A task counts only if the agent both passes its hidden suite and finishes within its per-task wall-clock budget.

| # | Capability | What it tests | Qwopus-Flash comparison | Comparison turns | Comparison wall | Qwopus-Flash result |
| --- | --- | --- | --- | ---: | ---: | --- |
| T01 | Multi-bug repair | Diagnose and fix 3 distinct bugs from a failing suite | ✅ pass | 10 | 55s | ✅ pass |
| T02 | Runtime debugging | Run a crashing script, read the traceback, and fix the root cause | ✅ pass | 8 | 57s | ✅ pass |
| T03 | Cross-file refactor | Rename a symbol and parameter across 4 files with zero stragglers | ✅ pass | 12 | 40s | ✅ pass |
| T04 | Build CLI to spec | New CLI with an exact stdout contract, verified by execution | ✅ pass | 15 | 124s | ✅ pass |
| T05 | Algorithm from spec | Bidirectional Roman numerals with full 1–3,999 round-trip | ✅ pass | 3 | 29s | ✅ pass |
| T06 | Performance optimization | O(n²) to sub-second on 20k inputs with identical results | ✅ pass | 15 | 129s | ✅ pass |
| T07 | Parser / interpreter | Recursive-descent expression evaluator without `eval()` | ✅ pass | — | — | ✅ pass |
| T08 | Self-correction | Recover correctly from a `UnicodeDecodeError` | ✅ pass | 6 | 38s | ✅ pass |
| T09 | Exact output contract | Strict schema, rounding, multi-key sort, and no mutation | ✅ pass | 3 | 24s | ✅ pass |
| T10 | Negative constraint | Hand-rolled CSV parser without the `csv` module | ✅ pass | 22 | 224s | ✅ pass |
| T11 | Test authoring | Write tests that catch 4 unseen buggy implementations | ✅ pass | 19 | 269s | ✅ pass |
| T12 | Messy-input parsing | Log parsing with continuations, junk lines, and nested brackets | ✅ pass | 7 | 60s | ✅ pass |
| T13 | Stateful persistence | KV store that survives a real process restart | ✅ pass | 4 | 36s | ✅ pass |
| T14 | Regression-safe fix | Fix an LRU-recency bug without breaking existing behavior | ✅ pass | 7 | 47s | ✅ pass |

#### Qwopus-Flash Inference Characteristics

| Metric | Value |
| --- | --- |
| Generation speed | 99.0 tok/s mean across tasks |
| MTP draft acceptance | 88.8% mean |
| Agent turns per task | 10.1 mean; 3–22 range |
| Output tokens per task | 2,340 mean; 30,414 total |
| Integrity violations | 0; hidden tests remained untampered after every task |

The Qwopus-Flash battery used **Qwopus 3.8 27B** in Q5_K_M GGUF format with a bundled NextN/MTP head, self-speculative decoding (`--spec-type draft-mtp`), q8_0 KV cache, and thinking disabled. It was run through headless Claude Code against a local llama.cpp server with real file and shell tools.

### 4.4 Reported Agent and Practical Workload Case Studies

These are workload case studies from the Qwopus-Flash card. They are individual reported workloads, not aggregate success rates or universal behavior claims.

#### Case Study A — Agent Workload Comparison

| Metric | Qwopus-Flash | Qwen3.8 base comparison |
| --- | --- | --- |
| Wall-clock | **640.2 s (10.7 min)** | 1,389.8 s (23.2 min) |
| Turns | **20, completed** | 48, crashed |
| Early-turn behavior | Normal | First turns hit 32K cap |
| Generated tokens | **27,975** | 109,337 |
| Average MTP acceptance | **80.1%** | 72.7% |
| Final status | **Completed** | 500 API error |
| Output | **40 KB / 1,319 lines** | 33 KB / 1,001 lines, partial state |

In this reported workload, the base comparison generated more tokens and spent more time but did not complete, while Qwopus completed with fewer turns and fewer generated tokens.

#### Case Study B — Long Code / Web-Generation Workload

| Metric | Qwopus-Flash | Qwen3.8 base comparison |
| --- | --- | --- |
| Completion tokens | **14,379** | 60,000 ceiling |
| Finish reason | **stop (complete)** | length (incomplete) |
| Thinking | **2,959 chars / 21 s** | 98,452 chars / 15.5 min |
| Answer | **51,844 chars, complete** | 70,116 chars, truncated |
| Wall time | **4.8 min** | 24.4 min |
| HTML | **All balanced** | Invalid / unclosed |

This case illustrates a reported valid long-form completion without hitting the token ceiling and with less reported internal reasoning. It does not establish that every web- or code-generation task will show the same ratio.

#### Case Study C — Long-Horizon Agent Workload

| Qwopus-Flash result | Value |
| --- | --- |
| Test outcome | **22 / 22 tests passed** |
| Wall time | 22.7 min |
| API time | 1,061 s |
| Turns | 56 |
| Tool calls | 55 |
| Tool-call mix | Bash 20 · Write 17 · Edit 11 · Read 7 |
| Tool errors | 5, all self-recovered |
| Input tokens | ~101K |
| Cumulative cache-read tokens | ~4.17M |
| Estimated emitted tokens | ~34.9K |

> [!IMPORTANT]
> These case studies are workload-specific evidence. They must not be converted into a general pass rate, API reliability guarantee, or claim that Qwopus is universally faster or more capable.

## 🎯 5. Recommended Use Cases

- Local MTP speculative decoding where decoder throughput and draft acceptance matter.
- Long-running agent workflows with repeated tool calls and iterative edits.
- Resource-conscious workloads where wall-clock time and generated-token cost are operational constraints.

## ⚠️ 6. Limitations

- **Python Formatting:** No formatting failures were observed in Kyle's reported temperature-0.3 Python-formatting check. This does not guarantee failure-free output on unseen prompts or other sampling settings. The training-data/verifier explanation remains a working hypothesis.

- **Accuracy–Efficiency Trade-off:** The Flash objective prioritizes practical inference efficiency. Qwopus-Flash and the Qwen base comparison use different reported settings and sample sets; the tables in Section 4 distinguish those scopes. They do not establish a controlled cross-version accuracy or speed improvement.
- **Reasoning Stability:** Although the long-tail behavior is improved in the reported evaluation, edge cases may still exhibit reasoning drift, loops, or inefficient trajectories.
- **Agent Dependence:** Tool-use quality and task completion remain dependent on the prompt, tool environment, orchestration layer, and feedback loop.
- **Experimental Release:** This is an independent experimental release for research, local evaluation, and technical exploration. It has not undergone broad safety evaluation or universal agent-reliability testing.

## 🙏 Acknowledgements

Special thanks to:

- **Qwen** for the Qwen3.8-27B base-model foundation.
- **Unsloth** for practical, efficient large-model fine-tuning tooling.
- [**Kyle Hessling**](https://x.com/KyleHessling1) for testing, evaluation support, and the coding-temperature and Python-formatting study.
- The open-source community for training tools, evaluation methods, and technical discussion.
