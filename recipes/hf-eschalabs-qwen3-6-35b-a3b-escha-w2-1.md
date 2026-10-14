# Qwen3.6-35B-A3B-Escha-W2 · SGLang · RTX 5090 32GB

[English](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.md) | [简体中文](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.zh-CN.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-07-22 · Numbers are quoted from the source and have not been re-run by this repo.

## Hardware

- RTX 5090 32GB (NVIDIA consumer)
- Reference cost: ≈ $5,400

## Model

- Qwen3.6-35B-A3B-Escha-W2 · `Escha W2`
- Download: [huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)

## Engine

- SGLang — install: https://github.com/sgl-project/sglang
- Note: SGLang

## Launch command

```bash
MEM=0.78 CTXLEN=32768 bash sglang/serve.sh
```

## Key parameters

- Context: 32K
- Concurrency: 2,670
- Tags: `2bit`, `8bit`, `MoE`

## Expected speed

- 283 tok/s decode (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed/relayed); your results may differ.
- Speed varies with drivers, engine version, context length and prompt length.

## Source & attribution

- [https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- Credit to the original author; this page only summarizes and links. Data under CC BY 4.0.
