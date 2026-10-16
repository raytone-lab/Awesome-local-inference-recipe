# Qwen3.8-27B · llama.cpp · RTX 5090 32GB

**English** | [简体中文](hf-byteshape-qwen3-8-27b-gguf-1.zh-CN.md) | [日本語](hf-byteshape-qwen3-8-27b-gguf-1.ja.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-08-18 · Numbers are quoted from the source and have not been re-run by this repo.

## Hardware

- RTX 5090 32GB (NVIDIA consumer)
- Reference cost: ≈ $5,400

## Model

- Qwen3.8-27B · `ShapeLearn mixed quantization GPU-1 (2.56 bpw, label IQ2_XXS)`
- Download: [huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)

## Engine

- llama.cpp — install: https://github.com/ggml-org/llama.cpp
- Note: llama.cpp (-np 1 -fa on)

## Launch command

```bash
llama-server -hf byteshape/Qwen3.8-27B-GGUF:<tag> --spec-type draft-mtp --spec-draft-n-max 3
```

Excerpt from the source (contains `...`/placeholders); see the source for full arguments.

## Key parameters

- Context: —
- Concurrency: single stream (-np 1)
- Tags: `2bit`, `dense`

## Expected speed

- 119.0 tok/s decode (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed/relayed); your results may differ.
- Speed varies with drivers, engine version, context length and prompt length.

## Source & attribution

- [https://huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- Credit to the original author; this page only summarizes and links. Data under CC BY 4.0.
