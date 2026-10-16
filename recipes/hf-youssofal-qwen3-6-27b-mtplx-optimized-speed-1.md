# Qwen3.6-27B-MTPLX-Optimized-Speed · MTPLX · MacBook M5 Max

**English** | [简体中文](hf-youssofal-qwen3-6-27b-mtplx-optimized-speed-1.zh-CN.md) | [日本語](hf-youssofal-qwen3-6-27b-mtplx-optimized-speed-1.ja.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-05-03 · Numbers are quoted from the source and have not been re-run by this repo.

## Hardware

- MacBook M5 Max (Mac)
- Reference cost: not published, see source

## Model

- Qwen3.6-27B-MTPLX-Optimized-Speed · `MLXCommunity 4-bit backbone + 3-bit draft LM head (MTP depth 3)`
- Download: [huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed](https://huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed)

## Engine

- MTPLX
- Note: MTPLX v0.1.0-preview

## Launch command

```bash
brew install youssofal/mtplx/mtplx && mtplx start
```

## Key parameters

- Context: —
- Concurrency: single request
- Tags: `3bit`, `4bit`, `dense`, `speculative`, `MTP`

## Expected speed

- 63.056 tok/s decode (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed/relayed); your results may differ.
- Speed varies with drivers, engine version, context length and prompt length.

## Source & attribution

- [https://huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed](https://huggingface.co/Youssofal/Qwen3.6-27B-MTPLX-Optimized-Speed)
- Credit to the original author; this page only summarizes and links. Data under CC BY 4.0.
