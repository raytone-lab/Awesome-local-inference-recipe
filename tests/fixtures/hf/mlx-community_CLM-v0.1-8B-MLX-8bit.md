---
license: apache-2.0
library_name: mlx
base_model: Qwen/Qwen3-8B
pipeline_tag: feature-extraction
tags:
- mlx
- apple-silicon
- contrastive
- clm
- embeddings
- verifier
---

# CLM-v0.1-8B for MLX (8bit)

An Apple-Silicon (MLX) port of **CLM-v0.1-8B**, the Contrastive Language Model from
[Contrastive-LM/CLM](https://github.com/Contrastive-LM/CLM): a frozen Qwen3-8B encoder plus two small
projection heads that score *states* against candidate *actions*. It answers typed questions
(yes/no, choice, score) and ranks candidates with a probability distribution, without generating text.

This is an **unofficial community port**, not released or reviewed by the CLM authors. It was checked
against upstream's reference implementation (the authors' code: vLLM + `clm-serve` at commit
`bb42c6c`, which we ran on an RTX 4090) on 778 questions; see *Parity* below.

The encoder itself is a standard MLX-format Qwen3-8B checkpoint, so its weights are usable with general
MLX tooling such as [mlx-workflow](https://www.connectcode.net/mlx-workflow.html) and its Mac app
[MLXUI](https://www.connectcode.net/mlxui_local_llm_ai_browser.html) for local, on-device inference.
Note that the CLM answer/rank behavior (the projection heads and `clm_mlx` code in this repo) is specific
to this port and isn't one of MLXUI's built-in model protocols — using it there would need custom
integration on top of the raw encoder.

| | |
|---|---|
| Encoder | Qwen3-8B @ `b968826d9c46`, MLX 8bit, `lm_head` removed (8.0 GB / 7.5 GiB) |
| Heads | CLM_v0.1-8B projection heads, float32 (the released weights, unchanged) |
| Pooling | last token, final hidden state after the last RMSNorm, L2-normalised |
| Max input | 2048 tokens; longer inputs keep the **first** 2048 (as the upstream server does) |
| Measured on | Apple M3 Pro, 18 GB: 336.1 tokens/s encoder throughput, 9.05 GB peak |

## Requirements

An Apple Silicon Mac (MLX), Python 3.10+, about 8 GB of disk and roughly 9.05 GB of free
memory while running (a 16 GB Mac is the practical minimum; measured peak above).

## Quickstart

```bash
pip install mlx mlx-lm transformers huggingface_hub
hf download mlx-community/CLM-v0.1-8B-MLX-8bit --local-dir clm-mlx && cd clm-mlx
```

Run Python from inside the downloaded folder (the `clm_mlx` package ships in it):

```python
from clm_mlx.engine import Engine
eng = Engine("encoder", "heads")
out = eng.answer(
    "Customer: my invoice was charged twice and nobody answers the phone!",
    {
        "urgency": {"type": "noul", "instructions": "Is this urgent?"},
        "department": {"type": "choice", "instructions": "Which team should handle this?",
                        "criteria": {"billing": "Charges, invoices, refunds", "technical": "Bugs and outages"}},
        "frustration": {"type": "score", "instructions": "How frustrated is the customer?",
                         "criteria": ["Calm", "Frustrated", "Very angry"]},
    },
)
print(out["answers"]["department"]["choice"], out["answers"]["department"]["probabilities"])
print(eng.rank("", ["The Moon's gravitational pull.", "Photosynthesis in plants."], "What causes tides on Earth?"))
```

Questions and answers use upstream's wire format (`noul` / `choice` / `score`); see the
[upstream API reference](https://github.com/Contrastive-LM/CLM#api-reference). Option projections are
cached, so repeated questions over new states only pay for the state.

## Parity with the upstream server

Reference: upstream's code, run by us on an RTX 4090 (vLLM 0.30.0, bfloat16), 882 texts
(2048-token limit included), 778 typed questions. The yardstick is how much the upstream
server disagrees **with itself**: its live answers compared with answers recomputed from its own vectors
for the same inputs.

| | this port vs upstream | upstream vs itself |
|---|---|---|
| top option agrees | **99.0%** | 98.6% |
| answer probability difference, p95 | 0.087 | 0.060 |
| answer probability difference, median | 0.036 | 0.022 |
| answer probability difference, max | 0.254 | 0.096 |
| encoder embedding cosine, min / mean | 0.9986 / 0.9997 | — |

Verdict: **within upstream noise** (top-option agreement at least upstream's own minus 1 point, and p95 difference
at most 1.5× upstream's). The port is somewhat noisier than upstream is with itself (p95, median and max above), while agreeing on the top option as often.
8 questions changed their top option; the upstream
server's own top probability on those was 0.35–0.54
(near-ties). The full report is in `parity.json`.

## Notes and limitations

- Encoder only: `lm_head` is removed, so this checkpoint **cannot generate text**.
- Inputs over 2048 tokens keep the first 2048, matching the upstream server. Upstream
  trained the heads on the *last* tokens of long states; `Engine(..., truncation="tail")` does that instead.
- Quantization adds a small amount of noise on top of upstream's own; decisions the upstream model is unsure
  about (near 50/50) can flip.

## Credits and licence

- CLM method, heads and reference implementation: Kwok, Kang, Suresh, Saad-Falcon, Pavone, Ré, Mirhoseini,
  *Contrastive Language Models: A System One Model for Fast and Generalizable Decision-Making* (2026),
  [contrastive-lm.notion.site](https://contrastive-lm.notion.site). Heads: [Contrastive-LM/CLM-v0.1-8B](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B), Apache-2.0.
- Encoder: [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B), Apache-2.0.
- This port (MLX conversion, `clm_mlx` code, parity harness): Apache-2.0.

```bibtex
@misc{kwok2026contrastivelanguagemodels,
  title={Contrastive Language Models: A System One Model for Fast and Generalizable Decision-Making},
  author={Jacky Kwok and Hangoo Kang and Tarun Suresh and Jon Saad-Falcon and Marco Pavone and Christopher Ré and Azalia Mirhoseini},
  year={2026}, note={Notion Blog}, url={https://contrastive-lm.notion.site}
}
```
