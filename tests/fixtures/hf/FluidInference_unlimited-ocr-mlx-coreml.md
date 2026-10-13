---
license: mit
base_model: baidu/Unlimited-OCR
base_model_relation: quantized
pipeline_tag: image-text-to-text
library_name: mlx
tags:
- mlx
- coreml
- apple
- ocr
- document-parsing
- multi-page
- deepseek-ocr
- moe
- fluidinference
---

# Unlimited-OCR (MLX + Core ML)

Baidu's [Unlimited-OCR](https://huggingface.co/baidu/Unlimited-OCR) (DeepSeek-OCR architecture: SAM-B + CLIP-L page
encoder, 12-layer DeepseekV2 MoE decoder, 3B parameters / ~0.5B active) for Apple silicon, including its
**multi-page mode**: up to 16 pages go in as one prompt and the whole document comes out of a single generation as
markdown, `<PAGE>`-separated, with `<|det|>label [x1, y1, x2, y2]<|/det|>` layout boxes (0–999 page coordinates).
Offline.

Two runtimes share the Core ML page encoder:

- **MLX decoder** (`mlx/`, recommended): 8-bit, upstream's R-SWA cache, ~200–260 tokens/s on an M5 Pro. Baidu's
  14-page paper in one pass: 13,420 tokens in ~70 s.
- **MLX turbo decoder** (`mlx-turbo/`): routed experts 4-bit (group 32), rest 8-bit. ~15% faster (14 pages in
  ~50 s, ~270 tokens/s); text within ~1 point of the 8-bit decoder, with small differences in formulas and tables.
- **Core ML decoder** (`UnlimitedOcrDecoder.mlpackage`): stateful 8-bit, ~50 tokens/s.

Runtime: `UnlimitedOcrFastManager` (MLX) and `UnlimitedOcrManager` (Core ML) in
[FluidUse](https://github.com/FluidInference/FluidUse) (Swift, macOS 15+), with a SwiftUI demo (`UnlimitedOcrDemo`):
drop a PDF, every page is read in one pass while the page thumbnails highlight the block being written.

## Packages

| File | Role | Size | Precision |
|---|---|---:|---|
| `UnlimitedOcrPageEncoder.mlpackage` | DeepEncoder + projector: one 1024 × 1024 page → 273 embeddings (16 rows of 16 + row newlines + view separator) | 0.8 GB | fp16 |
| `UnlimitedOcrDecoder.mlpackage` | decoder with a stateful K/V cache; functions `prefill_P{384,640,1152,2304}` (128 tokens per call) and `decode_P…` (1 token), weights shared | 2.7 GB | 8-bit weights (per block of 32), fp16 compute |
| `mlx/decoder.safetensors`, `mlx/config.json` | MLX decoder (embeddings, 12 layers, SwitchGLU experts, head) | 3.1 GB | 8-bit affine, group 64 |
| `mlx-turbo/decoder.safetensors`, `mlx-turbo/config.json` | same, routed experts at 4-bit | 2.1 GB | experts 4-bit group 32, rest 8-bit |
| `embeddings.f16` | input token embeddings for the Core ML decoder (host-side gather) | 0.3 GB | fp16 |
| `tokenizer.json`, `config.json` | tokenizer; shapes, buckets, prompt token ids | | |

Upstream's R-SWA attention keeps the whole prefix (prompt + page tokens) plus a ring of the last 128 generated tokens,
so the cache has a fixed size per prefix bucket: `k_cache` / `v_cache` are Core ML state, `[12 × (P + 128), 1280]`.
P = 384 / 640 / 1152 / 2304 holds 1 / 2 / 4 / 8 pages (each page is 273 tokens). Decoder inputs: `x [1, C, 1280]`
embeddings, `cos` / `sin [C, 128]`, additive `mask [1, 1, C, P + 128 + C]` (cached slots, then the C new tokens),
`write_idx [C]` cache slots, `out_index [1]`; outputs the top-16 logits of each vocab half. The host (Swift runtime is
the reference) assembles the prefix, places generated token t in slot `P + t % 128`, and applies upstream's 35-gram
no-repeat ban.

## Quality

Reference: upstream's own code (`trust_remote_code`), fp32 on CPU, greedy, same pixels.

| | vs upstream fp32 |
|---|---|
| 1 page (Baidu paper p. 4), 865 tokens | identical |
| 3 pages in one generation (p. 3–5), 2,461 tokens | identical text; 2 layout-box coordinates differ by 1 |
| 4-bit decoder (not shipped) | diverges at token 329 |

The page encoder must run on the GPU: on the Neural Engine its output is wrong (row cosine down to 0.66).

## Speed (M5 Pro, 24 GB, GPU, Swift)

| | |
|---|---:|
| page encoder | ~100 ms / page |
| prefill, 8 pages (2,189 tokens) incl. encoding | 3.0 s |
| decode | ~19 ms / token at 1 page, ~23 ms at 8 pages; flat over the whole read |
| Baidu paper, first 8 pages in one read: 6,727 tokens | 160 s (first release; ~17% less decode time per token since) |
| memory | 1.9 GB footprint + 2.7 GB mapped decoder weights |

The decoder computes all 64 experts per token (routing weights zero the unselected ones), which keeps the graph static
but reads every expert's weights on each step.

## Usage (Swift)

```swift
import FluidUse
import PDFKit
import UnlimitedOcrMLX

let manager = try await UnlimitedOcrFastManager.load(from: bundleDirectory)  // MLX; UnlimitedOcrManager = Core ML
let pdf = PDFDocument(url: pdfURL)!
let pages = try (0..<min(pdf.pageCount, manager.maxPages)).map {
    try UnlimitedOcrPagePreprocessor.page(from: pdf.page(at: $0)!)
}
var text = ""
for try await event in manager.read(pages: pages) {
    if case .text(let delta) = event { text += delta }
}
print(UnlimitedOcrDocument(parsing: text).markdown)
```

## License and credits

MIT, same as [baidu/Unlimited-OCR](https://huggingface.co/baidu/Unlimited-OCR) (`LICENSE` is Baidu's). All model
weights are Baidu's; this repository only changes their format and precision. Conversion by
[Fluid Inference](https://fluidinference.com).
