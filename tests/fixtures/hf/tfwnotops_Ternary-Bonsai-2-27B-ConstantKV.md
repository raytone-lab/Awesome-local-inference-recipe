---
license: apache-2.0
library_name: mlx
pipeline_tag: text-generation
base_model:
- tfwnotops/Ternary-Bonsai-2-27B-Crystal
tags:
- ternary
- mlx
- apple-silicon
- long-context
- constant-state
- kv-cache
- exact-store
- crystallized-attention
- mrail
---

# Ternary-Bonsai-2-27B-ConstantKV

<div align="center" style="line-height: 1;">
  <a href="https://doi.org/10.13140/RG.2.2.34347.40489" style="margin: 2px;"><img alt="Paper: Scarcity as Method" src="https://img.shields.io/badge/Paper-Scarcity%20as%20Method-C0392B" style="display: inline-block; vertical-align: middle;"/></a>
  <a href="https://doi.org/10.13140/RG.2.2.21299.18725" style="margin: 2px;"><img alt="Paper: Crystallized Attention" src="https://img.shields.io/badge/Paper-Crystallized%20Attention-6C4A9E" style="display: inline-block; vertical-align: middle;"/></a>
  <a href="https://doi.org/10.13140/RG.2.2.18140.35202" style="margin: 2px;"><img alt="Paper: Compute Once" src="https://img.shields.io/badge/Paper-Compute%20Once-8E6C8A" style="display: inline-block; vertical-align: middle;"/></a>
  <a href="https://github.com/DT-Foss/mrail" style="margin: 2px;"><img alt="GitHub mrail" src="https://img.shields.io/badge/GitHub-DT--Foss%2Fmrail-181717?logo=github&logoColor=white" style="display: inline-block; vertical-align: middle;"/></a>
</div>
<div align="center" style="line-height: 1;">
  <img alt="Attention state" src="https://img.shields.io/badge/attention%20state-1.18%20GiB%20at%20every%20length-2F5D8C" style="display: inline-block; vertical-align: middle;"/>
  <img alt="Cost" src="https://img.shields.io/badge/unseen%20books%2C%2032k-%2B0.0084%20nat-E0A33B" style="display: inline-block; vertical-align: middle;"/>
  <img alt="Pass keys" src="https://img.shields.io/badge/pass%20keys-40%2F40-3B8B5A" style="display: inline-block; vertical-align: middle;"/>
  <img alt="Mac mini" src="https://img.shields.io/badge/Mac%20mini%2016%20GB-32k%20tokens-8A8A8A?logo=apple&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
</div>

Ternary Bonsai 2 27B whose **attention state does not grow**. Each of the 16 full-attention layers of the Qwen3.8-27B
hybrid holds, from the first token on, 75.75 MiB: the exact band of the last 1,024 tokens, a crystallized carrier over
every far token, and an **exact store** of 8,192 keys and values per key-value head, admitted by the sharpest look each
token receives while it is still in the band. All 16 layers hold **1.18 GiB at every context length**; the native cache
of the same weights holds 3.2 GB at 32k tokens, 6.3 GB at 64k and 12.4 GB at 128k. At 32k tokens on eight unseen books
the state costs **+0.0084 nat per token** and retrieves **40 of 40 pass keys**, without training the model.

The whole model runs at **32k tokens on a Mac mini M4 with 16 GB**: peak 12.2 GB, 155–157 ms per token at 4k, 16k and 32k
tokens alike.

**Successor of [Ternary-Bonsai-2-27B-Crystal](https://huggingface.co/tfwnotops/Ternary-Bonsai-2-27B-Crystal).** The
weights (Prism ML's pack) and the crystallized heads are byte-identical to Crystal, on the same `.causal` graph (2,519
tensor bindings). What changes is the state: Crystal read the far past from a 4-bit index that grows with the context
(2.0 GB at 32k), or dropped it (`--top0`, 469 MiB, +0.116 nat). ConstantKV keeps a fixed exact store instead: the cost of
the index at a constant size. The method and every number on this card are from the paper **Scarcity as Method —
Attention, Replaced: Exact Forms, Constant State, and Reusable Inference** ([doi:10.13140/RG.2.2.34347.40489](https://doi.org/10.13140/RG.2.2.34347.40489), PDF in `paper/`).

## Original, Crystal, ConstantKV

Same weights, same tokenizer, same prompts; only the attention state of the 16 full-attention layers differs.

| | **Ternary Bonsai 2 27B** (native KV cache) | **Crystal** (index read) | **ConstantKV** (exact store) |
|:--|--:|--:|--:|
| weights | Prism ML pack | byte-identical | byte-identical |
| attention memory at 32k tokens | 3.2 GB | 2.0 GB | **1.18 GiB** |
| attention memory at 64k tokens | 6.3 GB | 3.5 GB | **1.18 GiB** |
| attention memory at 128k tokens | 12.4 GB | grows | **1.18 GiB** |
| cost on eight unseen books, 32k tokens (nat/token) | reference | +0.0045 | +0.0084 |
| pass keys retrieved (10 depths × 4k–32k) | 40/40 | 40/40 | **40/40** |
| exact lines, project-level code completion (40 items, 32k) | 0.473 | 0.474 | 0.442 |
| Mac mini M4, 16 GB, 32k tokens | – | – | **runs, peak 12.2 GB, 157 ms/token** |
| an answer the model has given before | computed again | route replay | **read from the map in 0.04–0.06 ms** |

The ternary weights themselves cost 0.28 nat per token against bf16 Qwen3.8-27B; the constant state adds a thirty-third
of that. Two independent implementations of the store (PyTorch and this MLX runtime) agree to within ±0.0004 nat on
every book:

| book | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| PyTorch | +0.0069 | +0.0097 | +0.0145 | +0.0091 | +0.0063 | +0.0077 | +0.0065 | +0.0064 |
| MLX runtime (this repository) | +0.0067 | +0.0099 | +0.0146 | +0.0093 | +0.0059 | +0.0080 | +0.0064 | +0.0063 |

<p align="center"><img src="https://huggingface.co/tfwnotops/Ternary-Bonsai-2-27B-ConstantKV/resolve/main/assets/constantkv/arch.png" width="100%" alt="Attention as it is and as it is replaced"/></p>
<p align="center"><sub>Figure 1 of the paper, one real query: the last token of a 32k-token PG19 book, layer 27, the six heads of one key–value group. (a) Softmax attention reads every key and value of the past. (b) The constant state reads the band exactly (blue), the 8,192 stored tokens at their native logits (red), and every other far token through the carrier (grey). The red caps are the peaks of attention the carrier cannot carry; the store holds exactly these tokens. Right: the state of one full-attention layer, to scale.</sub></p>

## What the state is

- **Band.** The last 1,024 tokens, exact keys and values (16.0 MiB per layer, plus 2.9 MiB of their index rows).
- **Carrier.** Every token that leaves the band enters a crystallized carrier: a key bias times five exponential decays
  with half-lives from a fixed catalogue, with a rank-8 query–key term, kept as a recurrent state (1.1 MiB per layer).
  These forms were found by the exact formula engine Wirkung, not designed.
- **Exact store.** 8,192 tokens per key-value head keep their exact keys and values in FP16 and are read at their native
  logits; their share of the carrier is subtracted, so nothing is counted twice (55.8 MiB per layer). A token is admitted
  by the sharpest single attention weight it receives from inside the band; the first token is always kept. Admission
  by window mass at the same size retrieves 33 of 40 pass keys, the sharpest look 40 of 40.
- **Exact below the store.** Up to 1,024 + 8,192 = 9,216 tokens the state is the native attention of the model.
- **A function of the tokens.** The state is determined by the tokens read; so the greedy answer of a context is a
  property of that context and can be stored once.

<p align="center"><img src="https://huggingface.co/tfwnotops/Ternary-Bonsai-2-27B-ConstantKV/resolve/main/assets/constantkv/store.png" width="100%" alt="Band, store and carrier"/></p>
<p align="center"><sub>Figure 5 of the paper: (a) one head, with the admission of a token that leaves the band by its sharpest look; (b) the constant state of one key–value group. In decoding, a token that leaves the band takes the slot of the weakest entry when its sharpest look is larger; two Metal kernels read the FP16 store in FP32.</sub></p>

<p align="center"><img src="https://huggingface.co/tfwnotops/Ternary-Bonsai-2-27B-ConstantKV/resolve/main/assets/constantkv/budget.png" width="100%" alt="Memory"/></p>
<p align="center"><sub>Figure 6 of the paper: (a) cost at 32k tokens against the size of the store, (b) cost by position in the book, (c) attention memory of the 16 full-attention layers against the context length. The carrier plus store stays flat; the native cache and the index grow.</sub></p>

## Answers that are not computed twice

The runtime keeps a `.mrail` map. Every answer is appended to it as a run; a request whose prompt the map has answered
before is read from the file in 0.04–0.06 ms, without touching the model, and identical to decoding on the backend that
wrote it (8 of 8 checked on CUDA; on the Mac, runs written by the Mac return identical). `maps/coding_constantkv.mrail`
ships 1,385 answers of this runtime to coding requests (0.97 MB), written on CUDA: decoded again on a Mac, 5 of 8 checked
runs are token-identical and the other three part at a near-tie, where the two best logits lie within 0.002–0.008.
`maps/coding_batch.mrail` adds 256 more as drafts. With `--draft on`, the tree decoder drafts the next tokens from the maps
and the running answer and verifies them in one pass; rejected branches are rolled back level-exactly without evaluating
a layer twice (DeltaNet and crystal state are rewritten from recorded inputs). On 60 held-out coding requests one
verified path accepts 1.18 tokens per pass without a map and **1.77 with the 1,641 runs**, still rising with the size of
the map. Every emitted token is the argmax of the model: drafts change the number of passes, never the output.

<p align="center"><img src="https://huggingface.co/tfwnotops/Ternary-Bonsai-2-27B-ConstantKV/resolve/main/assets/constantkv/maps.png" width="100%" alt="Maps"/></p>
<p align="center"><sub>Figure 11 of the paper: (a) accepted tokens per pass on unseen coding requests against the size of the map, for this model (red, blue) and for the compiled 1.5B; (b) more paths verified per pass on the 27B. The released decoder verifies one path.</sub></p>

## Quickstart

```bash
hf download tfwnotops/Ternary-Bonsai-2-27B-ConstantKV --local-dir constantkv
pip install -r constantkv/crystal_runtime/requirements.txt      # Metal on Apple Silicon, CUDA 12.9 on Linux
pip install --find-links constantkv/crystal_runtime "crystal_runtime==2.0.0"
python constantkv/crystal_runtime/quickstart_constantkv.py --pack constantkv \
    --prompt "Write a Python function that returns the n-th Fibonacci number iteratively."
```

`--file notes.txt --prompt "..."` puts a long document in front of the question; `--file code.py --complete` completes a
file; `--native` runs the same pack with the growing native cache for comparison; `--store` sets the store size. Your own
map lives in `~/.constantkv/maps/own.mrail` (started from the shipped one); asking the same thing twice returns the
answer from the file. Generation is greedy.

On a 16 GB Mac close memory-heavy apps before a 32k-token context: the runtime itself peaks at 12.2 GB.

Checked from this repository, freshly downloaded into a new environment: on a Mac mini M4 (16 GB, Python 3.11 and 3.13)
the monorail verifies every file, a known prompt returns from the map in 0.05 ms and a new one decodes at 8 tokens/s; on an
NVIDIA RTX PRO 6000 Blackwell (Python 3.11, CUDA) `eval/pg19_store.py` reproduces the measurement behind the table
above for book 6 at 32k tokens to the last digit (2.6237059 nat per token, 29 s), greedy decoding runs at 45.6 tokens/s, and the tree decoder
with the shipped maps accepts 2.39 tokens per pass with output identical to greedy.

## Files

| File | |
|:--|:--|
| `model.safetensors`, `config.json`, `tokenizer*`, `runtime/`, … | Prism ML's Ternary Bonsai 2 27B MLX pack, byte-identical (checked against the publisher's `files.json`); its model card is `README.bonsai.md` |
| `crystal.safetensors`, `crystal.json` | the crystallized heads (16 layers × 24 heads), byte-identical to Crystal |
| `causal/`, `bundle.json`, `inventory.pinned.json` | the monorail: `.causal` graph with 2,519 tensor bindings; `bundle.json` lists every shard and every file of this repository with SHA-256, and a modified or added byte is rejected at load time |
| `crystal_runtime/` | compiled MLX runtime 2.0.0 (constant state with the exact store, Metal store kernels, tree decoder with rollback, CUDA DeltaNet kernel, monorail, `.mrail`) as wheels for macOS and Linux, and the quickstart |
| `maps/` | `coding_constantkv.mrail` (1,385 answers of this runtime), `coding_batch.mrail` (256 answers, drafts only) |
| `eval/` | the evaluation scripts of the paper for this model (PG19, pass keys, Mac long context, decoder against greedy, draft replay) and their data: the eight PG19 books as token ids, the 60 held-out prompts, the greedy answers |
| `paper/` | Scarcity as Method |
| `assets/constantkv/` | the figures of this card, from the paper |

## Lineage

1. [Ternary-Bonsai-2-27B-Crystal](https://huggingface.co/tfwnotops/Ternary-Bonsai-2-27B-Crystal) — crystallized
   attention: carrier plus exact index correction, the first constant-state model of the line.
2. [Qwen2.5-1.5B-Instruct-HCGM](https://huggingface.co/tfwnotops/Qwen2.5-1.5B-Instruct-HCGM) — the same idea carried
   through a whole network: a transformer compiled into a causal graph with a 14.4 MiB state, 470 tokens/s on the Neural
   Engine of a Mac mini, answers as `.mrail` tracks.
3. **Ternary-Bonsai-2-27B-ConstantKV** — the 27B with a state that does not grow, at the quality of the index, on a
   16 GB Mac.

## Papers

- **Scarcity as Method — Attention, Replaced: Exact Forms, Constant State, and Reusable Inference**
  ([doi:10.13140/RG.2.2.34347.40489](https://doi.org/10.13140/RG.2.2.34347.40489), `paper/Foss_2026_Scarcity_as_Method.pdf`) — the program of work as one answer: the forms found by Wirkung, the laws
  that place a constant state, the exact store of this model, the compiled 1.5B, and inference that is reused.
- **[Crystallized Attention](https://doi.org/10.13140/RG.2.2.21299.18725)** — fixed-state carriers and exact index
  correction for the full-attention heads of a 27B hybrid.
- **[The Holographic Causal Graph Machine](https://doi.org/10.13140/RG.2.2.28206.68167)**,
  **[No GPU, No KV Cache](https://doi.org/10.13140/RG.2.2.31562.12484)** and
  **[Compute Once](https://doi.org/10.13140/RG.2.2.18140.35202)** — the compiler, the Neural Engine runtime and answers
  as reusable tracks.

## Citation

```bibtex
@misc{foss2026scarcity,
  author = {Foss, David Tom},
  title  = {Scarcity as Method. Attention, Replaced: Exact Forms, Constant State, and Reusable Inference},
  year   = {2026},
  doi    = {10.13140/RG.2.2.34347.40489}
}
@misc{foss2026crystal,
  author = {Foss, David Tom},
  title  = {Crystallized Attention: Fixed-State Carriers and Exact Index Correction for the Full-Attention Heads of a 27B Hybrid Language Model},
  year   = {2026},
  doi    = {10.13140/RG.2.2.21299.18725}
}
@misc{foss2026computeonce,
  author = {Foss, David Tom},
  title  = {Compute Once: Constant-State Language Models Make Answers Reusable and Agents Cheap},
  year   = {2026},
  doi    = {10.13140/RG.2.2.18140.35202}
}
```

## License

Weights: Prism ML, Ternary Bonsai 2 27B (Apache License 2.0), derived from Qwen3.8-27B (Apache License 2.0); crystal
parameters, monorail graph and maps: Apache License 2.0 (`LICENSE`, `NOTICE`). The compiled runtime in
`crystal_runtime/`: research license (`crystal_runtime/LICENSE`; free for non-commercial research and evaluation,
commercial use by license). The evaluation scripts in `eval/`: Apache License 2.0. The `.causal` format and the live
graph come from Immer. Author: David Tom Foss (d.foss@ieee.org, ORCID 0009-0004-0289-7154).
