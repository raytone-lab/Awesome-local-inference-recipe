---
license: apache-2.0
library_name: mlx
pipeline_tag: text-generation
tags:
- ternary
- 1.58-bit
- mlx
- mlx-swift
- apple-silicon
- on-device
- prismml
- bonsai
base_model:
- prism-ml/Ternary-Bonsai-8B-unpacked
---

<p align="center">
  <img src="./assets/bonsai-logo.svg" width="280" alt="Bonsai">
</p>

<p align="center">
  <a href="https://prismml.com"><b>Prism ML Website</b></a> &nbsp;|&nbsp;
  <a href="https://github.com/PrismML-Eng/Bonsai-demo/blob/main/ternary-bonsai-8b-whitepaper.pdf"><b>White Paper</b></a> &nbsp;|&nbsp;
  <a href="https://github.com/PrismML-Eng/Bonsai-demo"><b>Demo &amp; Examples</b></a> &nbsp;|&nbsp;
  <a href="https://discord.gg/prismml"><b>Discord</b></a>
</p>

# Ternary-Bonsai-8B-mlx-2bit

Ternary (1.58-bit) language model for Apple Silicon

> **7.1x** smaller than FP16 | **5.2x** faster on M4 Pro | **27** tok/s on iPhone | runs on Mac, iPhone, iPad

## Highlights

- **2.15 GiB** (2.30 GB) packed 2-bit size (down from 16.38 GB FP16) — runs comfortably on any Mac or iPhone
- **Ternary weights** {-1, 0, +1} across embeddings, attention projections, MLP projections, and LM head
- **75.5 avg** benchmark score across 6 categories — competitive with full-precision 8B models at 1/9th the size
- **5-point improvement** over our earlier 1-bit Bonsai 8B (70.5) at only ~0.6 GB additional footprint
- **MLX-native format** with group size 128 and FP16 scaling

<p align="center">
  <img src="./assets/frontier.svg" width="680" alt="Pareto Frontier">
</p>

## Resources

- **[White Paper](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/ternary-bonsai-8b-whitepaper.pdf)**
- **[Demo repo](https://github.com/PrismML-Eng/Bonsai-demo)** — examples for serving, benchmarking, and integrating Bonsai
- **[Discord](https://discord.gg/prismml)** — community support and updates
- **Kernels**: [MLX](https://github.com/ml-explore/mlx) (Apple Silicon) · [mlx-swift](https://github.com/ml-explore/mlx-swift) (iOS/macOS) — 2-bit format is supported out of the box

## Model Overview

| Item             | Specification                                                            |
| :--------------- | :----------------------------------------------------------------------- |
| Base model       | Qwen3-8B                                                                 |
| Parameters       | 8.19B (~6.95B non-embedding)                                             |
| Architecture     | GQA (32 query / 8 KV heads), SwiGLU MLP, RoPE, RMSNorm                  |
| Layers           | 36 Transformer decoder blocks                                            |
| Context length   | 65,536 tokens                                                            |
| Vocab size       | 151,936                                                                  |
| Weight format    | Ternary g128: {-1, 0, +1} with FP16 group-wise scaling                  |
| Packed 2-bit size| **2.15 GiB** (2.30 GB)                                                   |
| Ternary coverage | Embeddings, attention projections, MLP projections, LM head              |
| License          | Apache 2.0                                                               |

## Quantization Format: Ternary g128

Each weight takes a value from {-1, 0, +1}, with one shared FP16 scale per group of 128 weights:

```
w_i = scale_g * t_i,    t_i in {-1, 0, +1}
```

The information-theoretic cost is log2(3) ≈ 1.585 bits per weight, plus FP16 group scales (16 bits per 128 weights), for a theoretical minimum of ~1.71 bits/weight. This release uses the MLX 2-bit format, which stores each ternary value in 2 bits plus group scales, for an effective ~2.125 bits/weight.

The addition of a zero value compared to binary (1-bit) provides more expressive weight representations, allowing better preservation of model quality under extreme compression.

### Memory

| Format            | Size         | Reduction | Ratio      |
| :---------------- | ----------:  | --------: | ---------: |
| FP16              | 16.38 GB     | --        | 1.0x       |
| **MLX 2-bit g128**| **2.15 GiB** (2.30 GB) | **86.0%** | **7.1x**   |

## Quickstart

### MLX (Python)

> ```bash
> pip install mlx-lm
> ```

```python
from mlx_lm import load, generate

model, tokenizer = load("prism-ml/Ternary-Bonsai-8B-mlx-2bit")

response = generate(
    model,
    tokenizer,
    prompt="Explain quantum computing in simple terms.",
    max_tokens=256,
)
print(response)
```

### MLX Swift (iOS / macOS)

Ternary Bonsai 8B runs natively on iPhone and iPad via [MLX Swift](https://github.com/ml-explore/mlx-swift) at **27 tok/s** on iPhone 17 Pro Max. The 2-bit format is supported out of the box.

## Throughput (MLX / Apple Silicon)

| Platform              | Backend      | PP512 (tok/s) | TG128 (tok/s) | FP16 TG (tok/s) | Speedup    |
| :-------------------- | :----------- | ------------: | ------------: | ---------------: | ---------: |
| M4 Pro 48 GB          | MLX (Python) | 460           | 83            | 16               | **5.2x**   |

### iPhone 17 Pro Max (MLX Swift)

| Platform              | Backend    | PP512 (tok/s) | TG128 (tok/s) | 4-bit TG (tok/s) | Speedup    |
| :-------------------- | :--------- | ------------: | ------------: | ----------------: | ---------: |
| iPhone 17 Pro Max     | MLX Swift  | 363           | 27            | 14                | **1.9x**   |

## Benchmarks

Evaluated with EvalScope v1.4.2 + vLLM 0.15.1 on NVIDIA H100 under identical infrastructure, generation parameters, and scoring. All models are in the 6B-9B parameter range.

| Model                     | Size         | Avg      | MMLU-R | MuSR | GSM8K | HE+  | IFEval | BFCL |
| :------------------------ | ----------:  | -------: | -----: | ---: | ----: | ---: | -----: | ---: |
| Qwen 3 8B                 | 16.38 GB     | **79.3** | 83     | 55   | 93    | 82.3 | 81.5   | 81   |
| **Ternary Bonsai 8B**     | **1.75 GB**  | **75.5** | 72.6   | 56.2 | 91    | 77.4 | 81.8   | 73.9 |
| *1-bit Bonsai 8B (prior)* | *1.15 GB*    | *70.5*   | 65.7   | 50   | 88    | 73.8 | 79.8   | 65.7 |
| RNJ 8B                    | 16.63 GB     | **73.1** | 75.5   | 50.4 | 93.7  | 84.2 | 73.8   | 61.1 |
| Ministral3 8B             | 16.04 GB     | **71.0** | 68.9   | 53.8 | 87.9  | 72.6 | 67.4   | 75.4 |
| Olmo 3 7B                 | 14.60 GB     | **70.9** | 72     | 56.1 | 92.5  | 79.3 | 87.1   | 38.4 |

Ternary Bonsai 8B ranks **2nd** among all compared models despite being 1/9th the size.

## Intelligence Density

```
density = -ln(1 - score/100) / size_GB
```

| Model                     | Size        | Intelligence Density (1/GB) |
| :------------------------ | ----------: | --------------------------: |
| **Ternary Bonsai 8B**     | **1.75 GB** | **0.803**                   |
| *1-bit Bonsai 8B (prior)* | *1.15 GB*   | *1.062*                     |
| Qwen 3 8B                 | 16.38 GB    | 0.096                       |
| RNJ 8B                    | 16.62 GB    | 0.079                       |

## Limitations

- Only MLX 2-bit format is available at initial release; more formats for other backends coming soon
- Mobile power measurement is estimated rather than hardware-metered
- The full-precision frontier continues to advance; the ternary methodology is architecture-agnostic

## Citation

```bibtex
@techreport{ternarybonsai,
    title   = {Ternary Bonsai: 1.58-bit Language Models at 8B, 4B, and 1.7B Scale},
    author  = {Prism ML},
    year    = {2026},
    month   = {April},
    url     = {https://prismml.com}
}
```

## Contact

For questions, feedback, or collaboration inquiries: **contact@prismml.com**