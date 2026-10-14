# Ternary Bonsai 2 27B · llama.cpp (PrismML fork) · MacBook M5 Pro

**English** | [简体中文](hf-prism-ml-ternary-bonsai-2-27b-gguf-5.zh-CN.md) | [日本語](hf-prism-ml-ternary-bonsai-2-27b-gguf-5.ja.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-09-16 · Numbers are quoted from the source and have not been re-run by this repo.

## Hardware

- MacBook M5 Pro (Mac)
- Reference cost: not published, see source

## Model

- Ternary Bonsai 2 27B · `PQ2_0`
- Download: [huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)

## Engine

- llama.cpp (PrismML fork) — install: https://github.com/ggml-org/llama.cpp
- Note: PrismML llama.cpp fork

## Launch command

```bash
llama-cli ... -ngl 99 -fa on -c 32768
```

Excerpt from the source (contains `...`/placeholders); see the source for full arguments.

## Key parameters

- Context: -c 32768
- Concurrency: batch 1
- Tags: `ternary`, `dense`, `long-context`

## Expected speed

- 28.1 tok/s decode; 387 tok/s prefill (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed/relayed); your results may differ.
- Speed varies with drivers, engine version, context length and prompt length.

## Source & attribution

- [https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- Credit to the original author; this page only summarizes and links. Data under CC BY 4.0.
