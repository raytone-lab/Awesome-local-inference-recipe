---
library_name: mtplx
license: apache-2.0
pipeline_tag: text-generation
tags:
- mlx
- apple-silicon
- speculative-decoding
- qwen
- qwen3
- qwen3-next
- mtp
- mtplx
- local-ai
---

# Qwen3.6-27B MTPLX Optimized Speed

## Run this with MTPLX

**MTPLX** is an MLX-native runtime for native Multi-Token-Prediction speculative decoding on Apple Silicon. Up to **2.24× faster decode** at real coding temperatures (`temp=0.6 / top_p=0.95 / top_k=20`) using the model's own built-in MTP heads — no external drafter, no greedy hack.

```bash
brew install youssofal/mtplx/mtplx
mtplx start
```

**Project:** [github.com/youssofal/MTPLX](https://github.com/youssofal/MTPLX)

**Other MTPLX checkpoints:**

- [Qwen3.5-4B-MTPLX-Optimized-Speed](https://huggingface.co/Youssofal/Qwen3.5-4B-MTPLX-Optimized-Speed) — small 4-bit speed-test
- [Qwen3.5-4B-Optimized-MTPLX](https://huggingface.co/Youssofal/Qwen3.5-4B-Optimized-MTPLX) — small 8-bit

---

This is the speed checkpoint for MTPLX v0.1.0-preview. It combines the
and embeds `mtplx_runtime.json` so MTPLX can run it as the optimized speed
variant.

Target repository: `Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed`

## Runtime

```bash
mtplx pull Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed
mtplx run "hello" --model Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed
mtplx serve --model Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed --port 8000 --no-stats-footer
```

MTPLX v0.1.0-preview supports Qwen3-Next-MTP only. This model is verified for
the `qwen3-next-mtp` backend.

## Sources And Attribution

| Component | Source | Revision | License |
|---|---|---:|---|
| Base model | `Qwen/Qwen3.6-27B` | `6a9e13bd6fc8f0983b9b99948120bc37f49c13e9` | Apache-2.0 |
| MTPLX conversion and runtime contract | `youssofal/mtplx` | v0.1.0-preview.1 | Apache-2.0 |

The trunk is the MLXCommunity flat 4-bit affine conversion of
compressed-tensors checkpoint at the revision listed above.

## Verification

`mtplx_runtime.json` records:

- architecture: `qwen3-next-mtp`
- maximum MTP depth: `3`
- recommended profile: `sustained`
- recommended draft-only LM head: `3-bit affine, group_size=64`
- recommended draft sampler: temperature `0.70`, top-p `0.95`, top-k `20`
- exactness gate: `Phase 0H paged-verifier smoke`
- exactness max absolute diff: `0.0`
- verified hardware: `Apple M5 Max, 128 GB unified memory`
- verified timestamp: `2026-05-03T23:07:00+0100`

Target sampler used for the recorded contract: temperature `0.6`,
top-p `0.95`, top-k `20`, with thinking mode disabled. The draft proposal
sampler is intentionally slightly hotter at temperature `0.70`; target
verification and residual correction remain exact.

## Performance Honesty

This is the default speed lane. On the local Apple M5 Max fanmax
sustained benchmark, this artifact reached **63.056 tok/s** and
**62.886 tok/s** at depth 3 on the long-code 192-token prompt when using its
contract-recommended 3-bit draft-only LM head plus draft sampler temperature
`0.70`, with thinking mode disabled and foreground app load reduced. The
proposal change reduced the measured correction tokens from 6 to 3 and verify
calls from 50 to 49 on the recorded prompt; target sampling remains temperature
`0.6` / top-p `0.95` / top-k `20`. A full greedy diagnostic on the same cleaned
fanmax window measured **60.108 tok/s**. Earlier contract evidence measured
61.527 and 60.900 tok/s, the earlier 3-bit draft-head contract measured 60.038
and 60.061 tok/s, and the older 4-bit draft-only LM head measured 57.668 tok/s
on the same lane.

## Files

- `model-*.safetensors`: MLXCommunity flat 4-bit trunk shards.
- `mtp/weights.safetensors`: calibrated prequantized INT4 MTP sidecar, nested so generic MLX vision loaders only glob the base model shards.
- `mtplx_runtime.json`: MTPLX verified runtime contract.
- `MTPLX_PUBLISH_MANIFEST.json`: local staging manifest with source paths,
  materialization method, sizes, and optional hashes.

## Links

- **MTPLX**: [github.com/youssofal/MTPLX](https://github.com/youssofal/MTPLX)  ·  `pip install mtplx`
- **Base model**: [Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B)
