# Qwen3.6-35B-A3B-Escha-W2 · SGLang · RTX 5090 32GB

**English** | [简体中文](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.zh-CN.md) | [日本語](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.ja.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-07-22 · Numbers come from the source. This repo did not measure them again.

## Hardware

- RTX 5090 32GB (NVIDIA consumer)
- Reference cost: ≈ $5,400

## Model

- Qwen3.6-35B-A3B-Escha-W2 · `Escha W2 (INT8=on)`
- Download: [huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)

## Engine

- SGLang — install: https://github.com/sgl-project/sglang
- Note: SGLang (sglang/serve.sh)

## Launch command

```bash
MEM=0.78 CTXLEN=32768 bash sglang/serve.sh (on 5090 add INT8=on ATTN_BACKEND=triton MEM=0.82)
```

## Key parameters

- Context: 32K (16GB card 8K×16)
- Concurrency: single stream 283; bs32 about 2,670 (peak 3,017.6 @32 streams)
- Tags: `2bit`, `8bit`, `MoE`

## Expected speed

- 283 tok/s decode (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed or relayed). Your results can differ.
- Speed changes with drivers, engine version, context length, and prompt length.

## Source & attribution

- [https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- Credit to the original author. This page only summarizes and links. Data under CC BY 4.0.
