# Qwen-Image 2.1 (7B + 8B text encoder) · ComfyUI · RTX 4090 24GB

**English** | [简体中文](image-001.zh-CN.md) | [日本語](image-001.ja.md) · [← All recipes](../README.md)

> Source level: **✅ Measured** · Date: — · Numbers come from the source. This repo did not measure them again.

## Hardware

- RTX 4090 24GB (NVIDIA consumer)
- Reference cost: ≈ $2,214

## Model

- Qwen-Image 2.1 (7B + 8B text encoder) · `official Comfy-Org INT8 · ComfyUI`
- Download: not published. See the source

## Engine

- ComfyUI — install: https://github.com/comfyanonymous/ComfyUI

## Launch command

Command not published. See the source.

## Key parameters

- Context: native 2K
- Concurrency: single card, serial
- Tags: `8bit`

## Expected speed

- 8.1 s / 1024² (40 steps); 30.2 s / 2048×1152 (50 steps); peak 16.2GB (✅ Measured)

## Caveats

- Speed changes with drivers, engine version, context length, and prompt length.

## Source & attribution

- [https://x.com/yume_arasaki/status/2102176739359404499](https://x.com/yume_arasaki/status/2102176739359404499)
- Credit to the original author. This page only summarizes and links. Data under CC BY 4.0.
