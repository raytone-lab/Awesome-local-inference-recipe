---
license: apache-2.0
base_model: Cloudflare/clef-omni
base_model_relation: quantized
library_name: mlx
pipeline_tag: zero-shot-classification
tags:
- mlx
- clef
- cloudflare
- systemone
- structured-output
- classification
- multimodal
- audio
- video
- qwen3_omni_moe
- custom-code
- decision-model
---

# mlx-community/clef-omni-4bit

[Cloudflare/clef-omni](https://huggingface.co/Cloudflare/clef-omni) converted to MLX (4-bit) for Apple Silicon.

Clef-Omni is a 30B-A3B mixture-of-experts decision model built on the Qwen3-Omni thinker. It turns a state (text, JSON, images, **audio**, or **video with its soundtrack**) plus a schema of typed questions into a probability for every allowed option, in a single forward pass. **It is not a chat model**: `mlx_vlm.generate` and LM Studio would load the backbone but produce meaningless text. Use the bundled `clef_mlx.py` loader, which runs the backbone and the joint schema head.

## Which variant fits your Mac?

| Variant | Base | Download | Peak memory (1k / 4k / 14k tokens) | Latency (1k / 14k tokens) | 21 s video + sound | Minimum Mac RAM |
|---|---|---|---|---|---|---|
| **clef-omni-4bit (this repo)** | 30B-A3B | 19.8 GB | 20.3 / 20.8 / 22.2 GB | 0.19 s / 4.5 s | 2.8 s | 32 GB |
| [clef-omni-8bit](https://huggingface.co/mlx-community/clef-omni-8bit) | 30B-A3B | 35.0 GB | 35.6 / 36.1 / 37.5 GB | 0.26 s / 5.4 s | 4.6 s | 64 GB |

Measured on an M5 Max (128 GB), median of 3 runs. A 1 MP image takes about 0.3 s and a 30 s audio clip about 0.25 s. macOS lets the GPU use only about 70–75% of RAM by default, so the minimum RAM is higher than the peak. Only ~3B parameters are active per token, so Clef-Omni is faster than the dense 9B Clef-Flash on long prompts despite the bigger download.

## Usage

```bash
pip install "mlx-vlm>=0.7.6,<0.8" huggingface_hub av pillow   # no torch needed
```

Tested with mlx 0.32.3, mlx-vlm 0.7.6 and transformers 5.19 (tokenizer and the numpy Whisper feature extractor only). `clef_mlx.py` uses mlx-vlm internals, so it warns if you load it with an untested mlx-vlm minor version. `av` (PyAV) decodes audio and video files; `pillow` decodes images.

```python
import sys
from huggingface_hub import snapshot_download

path = snapshot_download("mlx-community/clef-omni-4bit")
sys.path.insert(0, path)
import clef_mlx

model = clef_mlx.load(path)
response = model.systemone({
    "model": "clef-omni",
    "state": "Our checkout started returning errors and orders are blocked.",
    "questions": {
        "department": {
            "type": "choice",
            "instructions": "Which team should handle the message?",
            "criteria": {"billing": "Payments or invoices", "technical": "Bugs or outages"},
        },
        "urgency": {"type": "score", "criteria": ["Can wait", "This week", "Today"]},
        "outage": {"type": "noul", "instructions": "Is a service down?"},
    },
})
print(response["answers"])
```

Images, audio, and videos go in `images` / `audio` / `videos`, as in the original. Each item can be a file path, URL, base64 data URL, or raw bytes. Images may also be PIL images, audio may be 16 kHz mono sample arrays, and videos may be RGB frame arrays sampled at 2 frames per second. Video files are sampled at 2 fps, and their soundtracks are heard alongside the frames when every video in the record has one.

```python
model.predict({
    "state": {"task": "Review the installation: a photo of the unit, a recording of it running, and a video of the fan."},
    "images": ["unit.jpg"],
    "audio": ["running.mp3"],
    "videos": ["fan.mp4"],
    "questions": {
        "label_visible": {"type": "noul", "instructions": "Is the model and serial number label visible in the photo?"},
        "sounds_normal": {"type": "noul", "instructions": "Does the unit sound like it is running smoothly, without rattling or grinding?"},
        "fan_running": {"type": "noul", "instructions": "Is the fan running in the video?"},
    },
})
```

Images, audio, and video can all be mixed in one record. See the [original model card](https://huggingface.co/Cloudflare/clef-omni) for the input format, question types, and benchmarks.

## Try it from the command line

`clef_mlx.py` runs on its own. From the downloaded repo it uses that repo by default; elsewhere pass `--model mlx-community/clef-omni-4bit`.

```bash
cd "$(hf download mlx-community/clef-omni-4bit --quiet)"
python clef_mlx.py predict \
  --state "Review the voicemail." --audio voicemail.wav \
  --questions '{"urgent": {"type": "noul", "instructions": "Is the caller reporting an urgent problem?"},
               "team": {"type": "choice", "criteria": {"billing": "Payments", "technical": "Outages and errors"}}}'
```

`--questions` takes JSON, a `.json` file, or `-` for stdin; `--request` takes a whole request body instead; `--image`, `--audio` and `--video` attach files (each repeatable). The output is the SystemOne response as JSON.

## Run a local SystemOne server

```bash
python clef_mlx.py serve --port 8000          # http://127.0.0.1:8000, local only by default
curl http://127.0.0.1:8000/v1/systemone -H "Content-Type: application/json" -d '{
  "model": "clef-omni",
  "state": "Checkout has been failing for every customer for the last hour.",
  "questions": {"urgent": {"type": "noul", "instructions": "Is this urgent?"}}
}'
```

- `POST /v1/systemone` takes the same request body as the Jev/SystemOne API (and the Workers AI `@cf/cloudflare/clef-omni` example) and returns the same response (plus `usage.latency_ms`), so existing SystemOne clients can point at your laptop. `GET /health` and `GET /v1/models` are also available.
- `images`, `audio`, and `videos` go in as data URLs (`data:audio/mpeg;base64,...`), raw base64, or http(s) URLs. Local file paths are not accepted over HTTP.
- Errors return JSON: `400` for invalid requests, `413` with "maximum context length" for inputs that don't fit. Add `"truncate": false` to a request (or start with `--no-truncate`) to get the `413` instead of truncation.
- Requests run one at a time on the GPU. There is no authentication: keep the default `127.0.0.1` binding unless you put your own proxy in front.
- For the [Decision Index](https://github.com/apolinario/decision-index), start with `--no-truncate` and use its `http` engine: `python -m decision_index run --engine http --option base_url=http://127.0.0.1:8000`.

## Limitations

- **Not a chat model.** Text generation tools (`mlx_vlm.generate`, LM Studio, Ollama) load the backbone but give meaningless output. Only `clef_mlx.py` runs the decision head.
- **No speech output.** The base model's talker and code2wav weights (speech generation) are not included. The reference implementation doesn't load them either.
- **Long inputs are truncated by default**, exactly like the reference implementation: the state is cut so the whole prompt fits in 64,000 tokens (the reference default). Pass `truncate=False` to `predict()`/`systemone()` to get a `clef_mlx.ContextTooLong` error instead, or change `max_length`. Video costs tokens fast: about 150–260 tokens per second of video depending on resolution (about 255/s for 720p and up), plus about 13 per second of audio.
- **One record per call.** There is no batching; requests run one after another.
- **Speed depends heavily on the chip.** Latencies above are from an M5 Max; long prompts on base M-series chips will be several times slower.
- **Custom code.** Like the original release, this repo ships Python (`clef_mlx.py`) that you import and run. Read it before use if that matters in your environment.

## Conversion

- Backbone: mlx-vlm 0.7.6 `qwen3_omni_moe`, 4-bit affine, group size 64 (4.93 bits per weight overall). The MoE routers (`mlp.gate`) are 8-bit. The vision and audio encoders are kept in bf16. The thinker `lm_head` is quantized too: the head only reads its rows for lexical option vectors, and keeping it in bf16 made no measurable difference.
- `talker.*` / `code2wav.*` (speech output, 7.1 GB in bf16) dropped; `enable_audio_output: false`.
- Joint schema head: `joint_head.safetensors` copied unchanged (bf16) and run by `clef_mlx.py`.
- `processor_config.json` / tokenizer files are the originals from Cloudflare/clef-omni. `clef_mlx.py` is torch-free and reimplements everything the reference gets from transformers' `Qwen3OmniMoeProcessor` and thinker:
  - the `Qwen2VLImageProcessor` / `Qwen2VLVideoProcessor` resizing and patching;
  - the audio placeholder lengths and the audio-in-video token interleaving;
  - the Qwen3-Omni 3D rotary positions, which use time-aligned video and audio positions (mlx-vlm's generic path does not do this).

  On the parity set, token ids and rotary positions match the reference exactly. Pixel values and log-mel features match to within one uint8 rounding step.

## Parity vs. official PyTorch implementation (bf16)

The reference is the official `joint_schema_model.py` (torch 2.11, transformers 5.10.2) in bf16 **on CPU**. On Apple MPS, that reference gives hidden states that disagree with an independent float32 numpy forward pass (cos 0.39 at the first token), while MLX and CPU torch both agree with it. So use CPU, not MPS, when checking this model against the reference on a Mac.

10 records, 23 questions: 3 text, 2 image (one with two images), 2 audio (wav + mp3, speech + tone), 2 video (silent; with a speech soundtrack, so audio-in-video), and 1 with image + audio + video together.

| Inputs | Questions | MLX bf16: top agrees / max abs Δprob | 8-bit | **4-bit (this repo)** |
|---|---|---|---|---|
| Text | 7 | 7/7 / 0.057 | 7/7 / 0.050 | **7/7 / 0.069** |
| Images | 5 | 5/5 / 0.005 | 5/5 / 0.003 | **5/5 / 0.010** |
| Audio | 4 | 4/4 / 0.003 | 4/4 / 0.008 | **4/4 / 0.016** |
| Video (with and without sound) | 4 | 4/4 / 0.045 | 4/4 / 0.026 | **4/4 / 0.042** |
| Image + audio + video | 3 | 3/3 / 0.005 | 3/3 / 0.025 | **3/3 / 0.061** |
| **All** | **23** | **23/23 / 0.057 (mean 0.009)** | **23/23 / 0.050 (mean 0.008)** | **23/23 / 0.069 (mean 0.015)** |

The encoders were also checked on their own. In float32, MLX and torch vision-encoder outputs agree to cos 0.9999. In bf16, image and audio encoder outputs agree to cos ≥ 0.9994 mean. Measured on an M5 Max (128 GB). This is a small spot-check, not a full benchmark run.

## License

Apache-2.0, following [Cloudflare/clef-omni](https://huggingface.co/Cloudflare/clef-omni) and [Qwen/Qwen3-Omni-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct).
