# Qwen3.8-Flash-Next-MLX-Serve-mixed-4 · mlx-serve · Mac Studio/MBP M4 Max 128GB

**English** | [简体中文](hf-ddalcu-qwen3-8-flash-next-mlx-serve-mixed-4-8bit-1.zh-CN.md) | [日本語](hf-ddalcu-qwen3-8-flash-next-mlx-serve-mixed-4-8bit-1.ja.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-08-27 · Numbers are quoted from the source and have not been re-run by this repo.

## Hardware

- Mac Studio/MBP M4 Max 128GB (Mac)
- Reference cost: not published, see source

## Model

- Qwen3.8-Flash-Next-MLX-Serve-mixed-4 · `mixed 4/8-bit (≈75 GB resident)`
- Download: [huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit](https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit)

## Engine

- mlx-serve
- Note: mlx-serve 26.8.11

## Launch command

```bash
mlx-serve --model ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit --serve
```

## Key parameters

- Context: 268,288
- Concurrency: serial single request
- Tags: `4bit`, `8bit`, `long-context`

## Expected speed

- 60.0 tok/s decode; 730.0 tok/s prefill (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed/relayed); your results may differ.
- Speed varies with drivers, engine version, context length and prompt length.

## Source & attribution

- [https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit](https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit)
- Credit to the original author; this page only summarizes and links. Data under CC BY 4.0.
