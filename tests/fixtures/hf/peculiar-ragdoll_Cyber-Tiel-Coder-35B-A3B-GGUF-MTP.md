---
license: mit
base_model:
  - huihui-ai/Huihui-Ornith-1.5-35B-A3B-abliterated
base_model_relation: quantized
pipeline_tag: image-text-to-text
library_name: gguf
language:
  - en
  - zh
tags:
  - gguf
  - llama.cpp
  - qwen35moe
  - moe
  - imatrix
  - unsloth-dynamic
  - mtp
  - speculative-decoding
  - agentic-coding
  - abliterated
  - uncensored
  - vision
---
> [GGUF without MTP here](https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF), [MLX version here](https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-MLX-oQ4e), and [MLX MTP version here](https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-MLX-oQ4e-MTP).

<div align="center">
  <img src="assets/cybertiel_banner_crt.gif" alt="CyberTiel — TielCoder 35B-A3B, abliterated and cyber-tuned" width="100%">
</div>

> ⚠️ **WARNING - Read before use**: Abliterated models like CyberTiel are able to say and do things other models refuse, including potentially harmful behaviours. By using CyberTiel, you agree to take full personal responsibility and liability for your use of it, its behaviour and generated content, and to show caution: it is entirely up to you as the user to ensure your use of CyberTiel is legitimate, legal and harmless, and that the model is safely sandboxed and monitored when running. Much like a knife, abliterated models like CyberTiel can be classified and used as either a tool or a weapon, depending on the context and use case. We carry forward [huihui's original usage warnings](https://huggingface.co/huihui-ai/Huihui-Ornith-1.5-35B-A3B-abliterated#usage-warnings).

# All power to all people

*CyberTiel* outcodes every other 35B-A3B at Q4 quantization (and spring-of-2026 frontier models), while engaging with offensive security work without hesitation or refusal. As a sweet spot between speed and ability, CyberTiel delivers agentic coding solves about 3-4x faster than 3.8-27B dense. This is the first time the frontier coder in this size/speed class is an uncensored model. If you need a safer censored alternative, go for *[TielCoder](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF)*.

> **CyberTiel is based on [Huihui-Ornith-1.5-35B-A3B-abliterated](https://huggingface.co/huihui-ai/Huihui-Ornith-1.5-35B-A3B-abliterated)**
> (an uncensored [Ornith-1.5](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B)),
> **re-quantized dynamically with our own cyber-weighted imatrix, carrying the
> [Sharp chat template](https://huggingface.co/peculiar-ragdoll/Qwen-Sharp-Chat-Templates) and a grafted
> multi-token-prediction head** inside the GGUF.

<div align="center">
  <img src="assets/cybertiel_bench_swe.gif" alt="SWE-bench-Live — problems solved, coding ability improved" width="100%">
</div>

SWE-bench-Live tests the model's ability to autonomously solve a set of real issues and bugs in large codebases, published continuously and recently, with hidden regression tests catching if you broke something trying to fix something. Doing well on SWE-bench-Live represents real world autonomous production coding ability: the opposite of "benchmaxxing" and answer memorization for programming work.

With its optimizations, *CyberTiel* Q4 (22GB) represents a new frontier in quantized 35B-A3B MoE coders, suitable to solve real-world programming problems at speed, even on low-power hardware with limited VRAM.

<div align="center">
  <img src="assets/cybertiel_bench_swe_speed.gif" alt="SWE-bench-Live — time per solve, effective speed maintained" width="100%">
</div>

Benchmarked at 4-bit quantization, CyberTiel thinks and talks less than Ornith-1.5 and Qwen3.6-35B-A3B, making it a faster coder at the same time as it manages to solve ~70% more real world coding problems than Ornith-1.5 and Qwen3.6. For comparison, this domain-specific ability increase is about 7x larger than the generational step from Qwen3.5-35B-A3B to its 3.6 successor.

<div align="center">
  <img src="assets/cybertiel_bench_cybench.gif" alt="Cybench unguided — agentic CTF: CyberTiel 15/43 flags, 35%" width="100%">
</div>

*CyberTiel* has real offensive capabilities: run unguided, with no hints and no judge, it captures the flag on 15 of the 43 Cybench CTF tasks (35%).

<div align="center">
  <img src="assets/cybertiel_bench_harmbench.gif" alt="HarmBench — refusals removed, 0% refusal" width="100%">
</div>

*CyberTiel* (unlike *TielCoder*) does not refuse on HarmBench: zero refusals across all 84 requests, sampled twelve at a time from each of HarmBench's seven categories — cybercrime and intrusion among them, alongside chemical/biological, illegal, harassment, misinformation, copyright and general harm.

<div align="center">
  <img src="assets/cybertiel_bench_mmlu.gif" alt="MMLU-Pro — bird-brained on world knowledge" width="100%">
</div>

*CyberTiel* and *TielCoder* sacrifice world knowledge for coding ability and speed: pick them for work, and pick something else (like [Nail](https://huggingface.co/peculiar-ragdoll/Nail-Qwen3.6-35B-A3B-GGUF)) for trivia or exams. The loss comes with the specialization, not with the abliteration: CyberTiel lands on exactly TielCoder's MMLU-Pro score.

## Abliterated: Willing, able and slightly unstable

**Abliteration**, also known as "uncensoring" or "ablation", is the suppression of refusal in LLMs. This model has undergone abliteration.

Unabliterated models sometimes wrongly refuse benign (harmless) requests. With CyberTiel you don't need careful wording to get your work done, and deliberation of refusal does not distract the model's attention or waste tokens, thus increasing its ability to perform legitimate work cleanly. This usually comes at the cost of some small corruption of the original model, which in the case of *CyberTiel* is more than balanced out by the advantages combined with the optimized imatrix and quant strategy, leading to a decisive gain on both SWE-bench-Live (agentic coding) and Cybench (offensive security ability).

HarmBench measures to what degree models refuse to produce language and behaviours that can be deemed harmful when applied maliciously. CyberTiel does not refuse on HarmBench. Models that are capable of these behaviours can be used for good or neutral purposes, so this benchmark is a measurement of specific capability that demands personal responsibility on behalf of the user deploying the model, not of inherent harmfulness.

**We strongly insist on you sandboxing this model at the operating system level**, limiting and controlling its access to execute code on your machine, and limiting/controlling the way it can access the internet. With refusals removed, this is not an ordinary coding agent: after a misinterpreted intention or a prompt injection from a hostile website or third-party code, this model can turn against you or others and cause real harm. If you do not understand this or how to effectively mitigate it, we recommend you use the very capable yet guardrailed [TielCoder](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF) instead.

## Run it

The MoE architecture makes *Tiel* fast, even on smaller GPUs with partial GPU offloading, and makes the context KV small in RAM (≈5 GB RAM for 262k context at 16-bit KV precision) compared to 27B dense. We do not recommend going below UD-Q4 simply to fit the whole model in VRAM: When you can fit the model and kv across your RAM+VRAM, pick a Q4 quant or larger that you can run with a sizable context (131k-262k) in at least q8_0 KV, for agentic coding and cyber work.

The "fits" column is about your **combined available RAM+VRAM**, after the OS and other processes take their share.

| file | size | fits | notes |
|---|--:|:--|---|
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q2_K_XL.gguf` | 12.7 GB | 16 GB | **THE LAST RESORT**; 2-bit gives up real ability and struggles with agentic coding. Use anything larger, wherever it fits |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-IQ3_XXS.gguf` | 13.6 GB | 16 GB | **the 16 GB pick** — significantly better than Q2_K_XL for under a gigabyte more |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q3_K_XL.gguf` | 17.2 GB | 24 GB | 3-bit with plenty of context room; prefer IQ4_XS below unless you need the extra ~1 GB |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-IQ4_XS.gguf` | 18.1 GB | 24 GB | 4-bit quality with the most context headroom of any 4-bit tier |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q4_K_S.gguf` | 21.3 GB | 24 GB | tight 4-bit; useful when Q4_K_M leaves too little context room |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q4_K_M.gguf` | 22.5 GB | 24 GB | the **benchmarked** tier (SWE-bench-Live + Cybench); prefer Q4_K_XL below — better for only ~0.3 GB more |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q4_K_XL.gguf` | 22.7 GB | 24-32 GB | **start here** — the best 4-bit tier, only ~0.3 GB over Q4_K_M; snug on 24 GB, comfortable on 32 |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q5_K_XL.gguf` | 27.0 GB | 32 GB | the **32 GB** pick |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q6_K_XL.gguf` | 32.2 GB | 48 GB | near-lossless; will not leave usable context on 32 GB |
| `Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q8_K_XL.gguf` | 38.8 GB | 48 GB | reference |
| `mmproj-BF16.gguf` | 0.9 GB | — | the **vision projector** — Ornith's own, unmodified; add it to any tier above to use images |

Each tier is its counterpart in the [non-MTP ladder](https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF) plus **~0.4 GB** of MTP head — the same block at the same precision (**Q3_K**) in every tier. The head only *drafts*, so we swept head precision from Q8_0 down to Q2_K and found draft acceptance flat (~82%); the head therefore ships small (Q3_K, quantized straight from the trained BF16 head) rather than riding the tier's own bit-width, saving ~0.5 GB/tier at no measurable cost to acceptance or speed.

```bash
hf download peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF-MTP \
  Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q4_K_XL.gguf mmproj-BF16.gguf --local-dir CyberTiel-MTP
llama-server -m CyberTiel-MTP/Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q4_K_XL.gguf \
  -ngl 99 --jinja --ctx-size 262144 --spec-type draft-mtp \
  --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0
```

`--spec-type draft-mtp` turns the head on at llama.cpp's defaults; `UD-Q4_K_XL` is the recommended ~22 GB 4-bit tier (the benchmarks were run at the near-identical `UD-Q4_K_M`). **Without `--spec-type draft-mtp` the head is dead weight** — llama.cpp ignores those tensors and you are running the base model carrying ~0.4 GB you didn't need, in which case take the [non-MTP ladder](https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF).

Sampling: the flags above are the recommended agentic-coding settings. For cybersecurity/CTF work, swap to `--top-k 40 --min-p 0.05` (same temperature and top_p), tested on Q4. This is a looser configuration leading to more divergent and exploratory thinking, which leads to more solutions on Q4 but might create issues and non-convergence on lower quants. You can also set them in a configuration file instead of on the launch command.

Budget: llama-server defaults to an unrestricted reasoning budget and unlimited output tokens per turn (`--reasoning-budget -1`, `--predict -1`), and that default is intentional for this model. A low `max_tokens` or reasoning budget degrades overall performance and will not necessarily make the model converge on the correct answer any faster. If you do need to cap them, we recommend `--predict 32768` and `--reasoning-budget 16384`, with `--reasoning-budget-message "Proceed to final answer"`. This model is much better than other 35B-A3B builds at spending fewer tokens and less time in total over the course of a problem — it knows when it needs to cook and when it is done — which makes high budgets, or no budget at all, both the safer and the better setting.

**Partial GPU offload.** If the tier you want does not fit your VRAM, do **not** lower `-ngl` — keep every
layer on the GPU and push only the *routed experts* to CPU with `--n-cpu-moe`:

```bash
llama-server -m CyberTiel-MTP/Cyber-Tiel-Coder-35B-A3B-MTP-UD-Q4_K_XL.gguf \
  -ngl 99 --n-cpu-moe 16 --jinja --ctx-size 65536 --spec-type draft-mtp \
  -fa on -ctk q8_0 -ctv q8_0 \
  --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0
```

Attention, the SSM layers, the shared expert and the router are only ~2.6 GB and fit
almost anywhere. `--n-cpu-moe` moves the routed experts and leaves the shared expert and router on
the GPU. Dropping `-ngl` instead would evict all of it together, which is the wrong trade. Each `+1` to `--n-cpu-moe` frees
about **0.5 GB** of VRAM, so start from the table below and step down while watching tokens/sec:

| VRAM | 8 GB | 12 GB | 16 GB | 20 GB | 24 GB |
|---|---|---|---|---|---|
| `--n-cpu-moe` (Q4, 64k context, q8_0 KV) | 33 | 25 | 16 | 8 | 2–4 |

**Never pass `--n-cpu-moe 41` on this ladder.** The MTP head is block 40 — a full MoE block with its own
routed experts — so 41 pushes the *draft head* to CPU, and the head runs on every decode step. That trades
away the speedup you came to this repo for. **40 is the maximum useful value**: it offloads the whole body
and leaves the head on the GPU.

The math, if your card isn't on the list: the always-resident 2.6 GB, plus 0.8 GB of KV at 64k, plus ~0.1 GB
of SSM state and ~0.8 GB of compute buffers, is a **~4.3 GB** fixed cost. Whatever VRAM is left over holds
0.49 GB of routed experts per layer, and the rest go to CPU:

```
--n-cpu-moe  =  40 - floor( (VRAM_GB - 4.3) / 0.49 )
```

Context is cheap on this architecture: only 11 of the 41 blocks carry attention (the rest are SSM, with a
fixed-size state), so KV costs ~22 KB/token at f16 — 0.8 GB for 64k with `-ctk q8_0 -ctv q8_0`, and 3.1 GB
even at the full 262k. Dropping `-fa on -ctk q8_0 -ctv q8_0` doubles that and costs you ~1.5 expert layers
on the GPU at 64k, so keep it. On Apple unified memory there is one pool, so skip `--n-cpu-moe` entirely and
just use `-ngl 99`.

**It can see.** CyberTiel inherits Ornith-1.5's vision tower — the `mmproj-BF16.gguf` projector is
Ornith's own, passed through unmodified.

```bash
llama-mtmd-cli -hf peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF-MTP:UD-Q4_K_XL \
  -ngl 99 --image screenshot.png -p "What does this do?"
```

## Use it

The recommended coding-agent harness for CyberTiel, with which the SWE-bench-Live results were achieved, is [Pi.dev](https://pi.dev). It is a lean, open source, extensible framework, that you can adapt to your own use and workflows using the coding agent itself.

For larger projects and complex multi-part work, we use an orchestrated subagent workflow with test-driven and spec-driven development: After interviewing you about what you want built, the orchestrator agent commissions subagents for recon and research, then writes up a plan document, design, and a spec, defining the scope and shape of the work. It then commissions an implementer with the needed context to implement one part of it, which is then reviewed by the next subagent, and then fixes and corrections are applied by yet another fresh-context agent, which are then re-reviewed, until the orchestrator is happy with the result. The task is then marked as done, and the orchestrator moves on to the next point. This has the advantage of keeping work scoped inside the usable context window of each agent, increasing quality and rigor when applied correctly. CyberTiel does not need this sort of workflow to function or deliver contained fixes or features, but it makes it possible for the model to tackle larger work that would otherwise be outside the capability of a 35B-A3B model with a 262k context window, thus extending its reach.

There exist plug-and-play extensions and tools that can be used with Pi for this kind of workflow, or you can build your own using the coding agent itself, including skills and system prompts for the different agents and different steps of the workflow.

For security work, give it a harness whose skills, plugins and tools encode the patterns and workflows you actually use — the model follows a well-worn path far better than it invents one.

## The multi-token-prediction head

CyberTiel's abliterated base ships **no** MTP head — abliteration is performed on a headless model
(`block_count 40`, no `nextn` block). So we **grafted one on**: Ornith-1.5's trained `nextn` head — the
same block that ships in [TielCoder's MTP ladder](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF-MTP) —
appended at block 40 and pinned to Q3_K in every tier (quantized straight from the trained BF16 head). The head *drafts* a token ahead of the main
model; llama.cpp verifies it in the same forward pass and keeps it only if it matches.

**Grafting an un-abliterated head onto an abliterated model is safe.** The head only proposes; the
abliterated main model **verifies every token** by rejection sampling, so the accepted stream is exactly
CyberTiel's own distribution — a draft head cannot reintroduce refusals, it can only change how fast
tokens arrive. And it drafts well despite never being trained on the abliterated weights: **82% of its
single-token drafts are accepted**, because abliteration is a small perturbation and next-token
prediction is largely preserved.

**What it did on our hardware.** Sweeping llama.cpp's two knobs on `UD-Q4_K_XL`, against the same model
with speculation switched off:

| `--spec-draft-n-max` | `--spec-draft-p-min` | tok/s | vs off | accepted |
|--:|--:|--:|--:|--:|
| — (off) | — | 78.2 | 1.00x | — |
| 1 | 0.0 | 94.3 | **1.21x** | 82.1% |
| 3 | 0.0 | 91.4 | 1.17x | 61.2% |
| 8 | 0.0 | 44.9 | 0.57x | 28.5% |
| 1 | 0.5 | 91.0 | 1.16x | 88.2% |
| 4 | 0.5 | 90.1 | 1.15x | 75.3% |
| 8 | 0.5 | 78.1 | 1.00x | 65.1% |

Those are our numbers on our box, not a specification. The gain comes from verifying several tokens in
one forward pass instead of decoding them one at a time, so it turns on how your hardware prices a
batched pass against a single-token one — which moves with the GPU, the tier, the context length, and
whatever else is resident. Here short drafts won and long greedy ones lost badly (the `p_min=0.0` column
collapses to 0.57x at `n_max=8`); `p_min=0.5` is the robust setting, staying at 1.0–1.16x across every
draft length.

**So sweep it, and judge by tok/s, not acceptance rate** — they come apart. Our highest-acceptance
setting (88%) was slower than our fastest (82%), because it bought that acceptance by drafting less.
Time it end to end against `--spec-type none` on prompts that look like your work. Reasonable defaults:
`--spec-draft-n-max 1 --spec-draft-p-min 0.0` for peak, or `--spec-draft-p-min 0.5` if you can't sweep.

## The CyberTiel imatrix

CyberTiel is quantized according to the Unsloth Dynamic strategy, through our custom **code- and cybersecurity-weighted importance matrix** — the same dynamic-quant pipeline
as [TielCoder](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-GGUF), differing only in the
calibration corpus. An imatrix is **not training data**: it
measures *which weights carry the load* under a representative input distribution, so `llama-quantize`
spends its precision there and lets rounding error fall where it matters least. Point that measurement
at cyber-and-code text, and the low-bit quant stays comparable to full precision on exactly the work this build is for. The
abliteration removes the refusals, the imatrix keeps cyber and coding ability intact at 4-bit and below.
**These MTP tiers reuse that exact matrix, unchanged** — the grafted head lives in tensors an importance
matrix never covers, so it changes nothing about how the body is quantized.

Since Unsloth has not published quants for Ornith-1.5-35B-A3B (or their calibration corpus) at the time of writing, we benchmarked our imatrix quants against theirs on Qwen3.6-35B-A3B, which is Ornith's base. On mean KL divergence the two are on par. The more telling measure is the tail: the *99.9th-percentile* KL — the worst 0.1% of token positions, where a quant drifts furthest from full precision, and where an imatrix mismatch would show up if it were hiding behind a good average. There our matrix is ahead of Unsloth's at every tier from 5-bit down to 2-bit on **cybersecurity**, the domain it was calibrated for. On the out-of-domain holdouts the two trade places tier by tier, the one visible gap being documentation at 4-bit, where Unsloth's tail is cleaner. These are single-run percentiles with no error bars, so read them as *no tail-risk penalty for the specialization* rather than as a ranking.

<div align="center">
  <img src="assets/kl_q999_cybersec.png" alt="Cybersecurity-domain 99.9th-percentile KL divergence to a shared Q8_0 reference across UD tiers Q2→Q5_K_XL: CyberTiel's cyber-weighted imatrix quant against Unsloth's published UD quant of the same Qwen3.6-35B-A3B base — the model's own specialization; our tail is below Unsloth's at every tier" width="100%">
</div>

<div align="center">
  <img src="assets/kl_q999_code.png" alt="Code-domain 99.9th-percentile KL divergence to a shared Q8_0 reference across UD tiers Q2→Q5_K_XL: CyberTiel's cyber-weighted imatrix quant against Unsloth's published UD quant of the same Qwen3.6-35B-A3B base — the tail tracks the mean, the two curves staying together down the ladder" width="100%">
</div>

<div align="center">
  <img src="assets/kl_q999_documentation.png" alt="Documentation-domain 99.9th-percentile KL divergence across UD tiers Q2→Q5_K_XL: CyberTiel cyber-imatrix quant vs Unsloth's published UD quant of the same base, tail-risk curves overlapping down the ladder" width="100%">
</div>

<div align="center">
  <img src="assets/kl_q999_multilingual.png" alt="Multilingual-domain 99.9th-percentile KL divergence across UD tiers Q2→Q5_K_XL: CyberTiel cyber-imatrix quant vs Unsloth's published UD quant of the same base, tail-risk curves overlapping down the ladder" width="100%">
</div>

**Calibration corpus:** ≈50 MB (~50 M characters), matched to TielCoder's corpus depth so the two imatrices are
comparable, assembled entirely from public, redistributable security engineering and code:

| bucket | share | what it is | source |
|---|--:|---|---|
| **Security** | 40% | the specialization: half **offensive** (PoC / exploit code), half **defensive** (methodology, tooling, detection rules) | exploit-db · PayloadsAllTheThings · HackTricks · nuclei-templates |
| **Code** | 27% | hold general coding ability through the quant | eaddario `code_medium` + `code_large` |
| **Agentic tool-use** | 18% | the model is driven by a coding agent — real tool-call / bash-session traces | eaddario `tools_large` |
| **General + multilingual** | 15% | keep language and broad-knowledge pathways alive; non-Latin scripts (zh / ja / ko / ru / ar) weighted **2.5×**, since public offensive-security text is English by measurement | eaddario `combined_*` |

Buckets are **interleaved** as ~2 KB fragments, round-robin by budget, rather than concatenated in
blocks — so every calibration chunk sees a code + security + prose mix and no bucket gets over-weighted
by wherever a chunk boundary happens to land.

**Build** — generated with `llama-imatrix` over **800 chunks × 512 tokens** (~410 K token-passes,
`-ngl 99`) on a Q8_0 of the ablated Ornith BF16 (BF16 is 69 GB — too large to hold resident on a 64 GB machine; Q8_0 is the near-lossless imatrix standard). Final calibration perplexity **6.08**. The resulting
**192 MB** importance matrix drives every shipped UD tier (Q2_K_XL → Q8_K_XL), each quantized from the
ablated BF16 under the same Qwen3.6 / Ornith per-tensor *unsloth-dynamic* policy TielCoder uses. Same
recipe, same template — so the benchmark delta against TielCoder isolates the abliteration + cyber
imatrix, not the quant strategy.

**Both matrices are published in the [non-MTP GGUF repo](https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF)** — `Cyber-Tiel-Coder-35B-A3B.imatrix.gguf` (800 chunks, ~410 K token-passes, the matrix every shipped tier was quantized from) and `Cyber-Tiel-Coder-35B-A3B-fullcorpus.imatrix.gguf`, a second pass over the **entire** ~50 MB corpus (27,513 chunks × 512, ~14 M token-passes). At Q2 and Q4 they produce near-identical quants — the full-corpus matrix edges the 800-chunk one slightly on general code and is a wash on cybersecurity — so 800 chunks already captures everything this domain corpus routes to. Point `llama-quantize --imatrix` at whichever you prefer.

*The most interesting finding* is that — in comparison to TielCoder — our cyber-weighted imatrix (in combination with abliteration) cleanly and significantly increases *Tiel*'s performance on standard real-world software engineering tasks outside the training data, from the level of Opus 4.6 medium (12, where its TielCoder counterpart sits) to a 3-seed mean of 13.7 / 25 — above both — measured on SWE-bench-Live.

## Benchmarks disclaimer

The results can be seen in the introductory visualizations. **They were measured on the non-MTP body**
— the grafted head changes decode *speed* (see the sweep above), not what the model solves, since the
accepted stream is identical to the non-MTP model's.

All 35B-A3B-based models in the benchmark ran with a 75–80 tok/s base generation rate, and Qwen3.8-27B with a 22 tok/s generation rate. Both of these rates decrease as the model climbs towards the context ceiling. The time per solve on SWE-bench-Live is affected both by generation speed and the time it takes to run tool calls on my machine, and these factors will differ on other hardware. The part of speed that is not hardware dependent is the model's ability to converge quickly on a correct solution and deliver it, and this — in combination with chat template tricks — is Tiel's main speed advantage against the other 35B-A3B models. The relative difference between the models on your hardware will depend on both factors: If you run Tiel with partial GPU offloading but 27B entirely in VRAM because it is slightly smaller, the relative speed will change.

For increased validity, we ran CyberTiel three times on SWE-bench-Live. The three passes resolved 15, 13 and 13 problems out of the 25-problem set (mean 13.7). This variance across attempts is an artifact of the inherent variability and indeterminism of LLMs running at non-zero temperature. If we had the GPU-time and tokens, we would run all models at more seeds and problems across all benchmarks for maximal cross-comparison statistical validity, so take results as a strong indicator rather than a perfect comparison.

**On the Cybench task set.** Cybench is published as a 40-task benchmark, but the [public repository](https://github.com/andyzorigin/cybench) does not ship all 40: nine of the official tasks are Glacier CTF challenges whose files are not distributed with it. It does ship twelve *additional* tasks — from the same competitions (HackTheBox Cyber Apocalypse 2024, Sekai CTF 2022/2023, HKCert CTF 2022), with full metadata, subtasks and human first-blood times — that are not on the official 40 list. We ran every task the repository actually ships: 43 = 31 of the official 40, plus those 12. **15/43 (35%) is therefore not directly comparable to a published Cybench score**; restricted to the 31 official tasks alone, CyberTiel captured 10 flags. The runs are *unguided* — no subtask hints, no judge, exact final-flag match only — capped at 15 agent iterations, at 262k context with the CTF sampling settings given above.

This account and the models published are a non-profit project, and we intentionally decline offers of donations in order to ensure the independence and validity of our published results and products.

## Credits

- [**huihui-ai**](https://huggingface.co/huihui-ai/Huihui-Ornith-1.5-35B-A3B-abliterated) — the abliterated base this quantizes (refusals removed from Ornith-1.5).
- [**ornith-ai**](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B) — the underlying Ornith-1.5-35B-A3B weights, vision tower, and the trained MTP head this grafts on (MIT).
- [**Unsloth**](https://huggingface.co/unsloth) — the Dynamic GGUF quantization method this reproduces.
- [**froggeric**](https://huggingface.co/froggeric/Qwen-Fixed-Chat-Templates) — the template lineage Sharp builds on.
- [**eaddario**](https://huggingface.co/datasets/eaddario/imatrix-calibration) — the code, tool-use and multilingual calibration corpora the imatrix was measured on (MIT).
- Security calibration sources — [Exploit-DB](https://gitlab.com/exploit-database/exploitdb), [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings), [HackTricks](https://github.com/HackTricks-wiki/hacktricks), [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) — the public security engineering that formed the cyber bucket.
- [**llama.cpp**](https://github.com/ggml-org/llama.cpp) — `llama-quantize` / `llama-imatrix` / `llama-server` (and `--spec-type draft-mtp`).

MIT, inheriting Ornith-1.5's license.

## Citation

```bibtex
@misc{Cyber-Tiel-Coder-35B-A3B-GGUF-MTP,
  title  = {Cyber-Tiel-Coder-35B-A3B-GGUF-MTP},
  author = {Saga Ishtardottir},
  year   = {2026},
  url    = {https://huggingface.co/peculiar-ragdoll/Cyber-Tiel-Coder-35B-A3B-GGUF-MTP},
  note   = {Huihui-abliterated Ornith-1.5-35B-A3B, dynamically re-quantized with a cyber-weighted imatrix, carrying the Sharp chat template and a grafted Ornith MTP head for speculative decoding}
}
```
