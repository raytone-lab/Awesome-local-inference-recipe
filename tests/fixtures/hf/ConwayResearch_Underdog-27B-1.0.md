---
library_name: mlx
license: apache-2.0
pipeline_tag: image-text-to-text
tags:
- mlx
- 4-bit
- qat
- splash
---

# Underdog-27B-1.0

Underdog-27B by Conway is a 27-billion-parameter model for conversation, writing, coding, and everyday assistance. Its MLX 4-bit QAT weights pair with Splash's speculative decoding for responsive local generation on Apple Silicon. We finetuned this model to run better in Underdog for human users, based on Qwen3.8.

## Run with Splash

Install Splash 1.1.0 or later and authenticate with Hugging Face using an account with access to this repository. Then run:

```bash
hf auth login
splash serve --model ConwayResearch/Underdog-27B-1.0 --default-reasoning-effort medium
```

Splash automatically prepares the model and its compatible acceleration draft. Use the built-in chat interface or connect a compatible app. Medium reasoning is the recommended interactive default.

## Local generation speed

| Task | MLX-LM | Splash + DFlash2 | Generation speedup |
| --- | ---: | ---: | ---: |
| Email writing | 33.1 tokens/s | 80.6 tokens/s | 2.44x |
| Python coding | 33.0 tokens/s | 130.1 tokens/s | 3.94x |
| Long-document summarization | 32.5 tokens/s | 71.4 tokens/s | 2.20x |

Measured on an Apple M5 Max with 40 GPU cores and 48 GiB unified memory, macOS 26.5.1, using MLX 0.32.0 / MLX-LM 0.31.3 and Splash 1.1.0. Both configurations use the same MLX 4-bit weights. Values are mean decode rates from two runs per task, with temperature 0, reasoning set to `none`, a 512-token output budget, and no reused prompt tokens. Splash uses DFlash2 and INT8 KV; MLX-LM uses standard generation without a draft model. Engines were measured separately. Input lengths were 43, 44, and 3,003 tokens; generated output lengths may differ. Loading and warmup are excluded. Interactive medium reasoning is configured separately from these measurements.

## Run with MLX

Download the complete repository and select its local directory in a compatible MLX runtime. Keep the supplied weights, tokenizer, configuration, and chat template together. The complete model download is approximately 16.08 GB; Splash manages its acceleration draft separately.

This release includes fine-tuning and quantization-aware training by Conway. The original license is preserved in `LICENSE`.
