---
license: apache-2.0
base_model: BAAI/AREX-2
base_model_relation: quantized
library_name: mlx
pipeline_tag: image-text-to-text
language:
- en
tags:
- mlx
- apple-silicon
- mac
- quantized
- 6-bit
- arex-2
- qwen3.8
- vision
- agent
- reasoning
- tool-use
- deep-research
- long-context
---

# mlx-community/AREX-2-6bit

**AREX-2 for Mac.** This is [BAAI/AREX-2](https://huggingface.co/BAAI/AREX-2) converted to run on Apple Silicon Macs.
AREX-2 is an open model for coding, reasoning and agent work, and it can read images as well as text. This is the
6-bit version, converted to MLX format with mlx-vlm 0.7.4.

- **Original model:** [BAAI/AREX-2](https://huggingface.co/BAAI/AREX-2), built on Qwen3.8-27B
- **Size:** 27 billion parameters, 23 GB download
- **Takes in:** text and images. **Gives back:** text
- **Thinks before answering,** and supports tool calling
- **License:** Apache 2.0

## Speed and quality

| Size | Writing speed | With a speed helper | Match to the original | Hard problems solved, first try | Within 3 tries |
|---|---|---|---|---|---|
| 4-bit | 14 tokens/s | 27 tokens/s | 91.4% | 3 of 12 | 9 of 12 |
| 5-bit | 12 tokens/s | 20 tokens/s | 95.9% | 8 of 12 | 11 of 12 |
| **6-bit** | **10 tokens/s** | **19 tokens/s** | **97.6%** | **9 of 12** | **10 of 12** |
| 8-bit | 8 tokens/s | 19 tokens/s | 99.1% | 7 of 12 | 12 of 12 |

- **Measured on a Mac mini M4 Pro with 64 GB.** A token is about three-quarters of a word. Reading a prompt runs at about 90 tokens per second at every size.
- **Loading** took 18 to 33 seconds depending on size (26 for this one), from an external SSD.
- **Speed helper:** a small draft model that guesses ahead. See "Speed with a draft model" below.
- **Match to the original:** how often the build picks the same next word-piece as the full-size model.
- **Hard problems:** 12 Python problems, with up to 3 tries each and a 4,000-token limit. One run per size, so a gap of one or two is noise. With an 8,000-token limit the 4-bit solved 8 of 12 hard problems on the first try (the 5-bit: 11 of 12 at the same limit); with 4,000 it solved 3.

## Which size should I download?

| Your Mac's memory | Get this one | Download | Memory it used | In short |
|---|---|---|---|---|
| 24 GB | [4-bit](https://huggingface.co/mlx-community/AREX-2-4bit) | 16 GB | 16 to 24 GB | Smallest. Needs a response limit of 8,000 tokens or more, so it is the slowest to finish an answer. |
| 32 GB | [5-bit](https://huggingface.co/mlx-community/AREX-2-5bit) | 19 GB | 20 to 28 GB | Scored about the same as the 6-bit and 8-bit in the tests, in the least memory. |
| **48 GB** | **[6-bit](https://huggingface.co/mlx-community/AREX-2-6bit)** | **23 GB** | **23 to 31 GB** | **Slightly closer to the original, a little slower.** |
| 64 GB or more | [8-bit](https://huggingface.co/mlx-community/AREX-2-8bit) | 30 GB | 30 to 38 GB | Closest to the original, slowest. |

- **Memory it used** was measured on a 64 GB Mac, from a short chat up to a very long prompt (32,000 tokens).
- **The Mac sizes in the first column are estimates** from that memory use. Nothing was run on a smaller Mac.

## How to run it

**Easiest: LM Studio, no coding**

1. Install [LM Studio](https://lmstudio.ai) and open it.
2. Open its model search and paste `https://huggingface.co/mlx-community/AREX-2-6bit`.
3. Click Download. It is 23 GB.
4. Start a new chat, choose AREX-2 in the model picker, and wait for it to load.
5. Type your question. To ask about a picture, attach it to your message.

**Command line**

Install once:

```bash
pip install -U mlx-vlm
```

Ask a question. The first run downloads the model (23 GB):

```bash
python -m mlx_vlm.generate \
  --model mlx-community/AREX-2-6bit \
  --max-tokens 4000 --temperature 1.0 --top-p 0.95 --top-k 20 \
  --prompt "Write a Python function that merges overlapping intervals."
```

Ask about a picture by adding `--image`:

```bash
python -m mlx_vlm.generate \
  --model mlx-community/AREX-2-6bit \
  --max-tokens 4000 --temperature 1.0 --top-p 0.95 --top-k 20 \
  --prompt "What is in this picture?" --image photo.png
```

**From other apps and agent harnesses**

Start LM Studio's local server (the Developer tab, or `lms server start`). Any app that speaks the OpenAI API can then
use `http://localhost:1234/v1` with this model, including tool calls and images.

**Which apps it runs in**

| App | Status |
|---|---|
| LM Studio 0.4.8 | Tested: text, images and tool calls |
| mlx-vlm 0.7.4 (command line and Python) | Tested: text, images and tool calls |
| mlx-lm 0.32 | Tested: text only |
| mlx-dspark 0.20.1 | Tested: text, with a speed helper |
| MiniMax Code 0.5.9 (agent harness) | Tested on the 8-bit: it fixed three small failing projects using its own file and shell tools, in 6 of 6 trials. Served through mlx-dspark with thinking off. |
| Other agent harnesses and coding tools | Should work. Tool calling works, and LM Studio's local server returns standard tool calls, which is what most harnesses use. Not tested. |
| Jan, Msty and other apps with an MLX engine | Not tested. They load MLX models, so they may work. Image input depends on the app. |
| Ollama, llama.cpp and other GGUF apps | These need a different format. Use a GGUF build such as [bartowski/BAAI_AREX-2-GGUF](https://huggingface.co/bartowski/BAAI_AREX-2-GGUF). |

**Two settings that matter**

- **Leave the sampling at the model's defaults:** temperature 1.0, top-p 0.95, top-k 20. Do not set temperature to 0. (If you turn thinking off, Qwen's guidance for the base model is temperature 0.7, top-p 0.8, top-k 20; that was not tested here.)
- **Give it room to answer.** The model thinks before it replies, and a hard problem can take 1,000 to 4,000 tokens of thinking. If answers get cut off, raise the response limit (max tokens) to 4,000 or more.

## What the tests showed

- **The 5-bit, 6-bit and 8-bit are too close to tell apart.** The 4-bit is clearly weaker on hard problems.
- **AREX-2 was more efficient than plain Qwen3.8-27B:** about 46% fewer tokens and about half the time on the same tests.
- **It can run more than twice as fast with a speed helper.** The DFlash2 helper for Qwen3.8-27B ([incoai/Qwen3.8-27B-DFlash2](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2)) works with AREX-2 as it is. In mlx-dspark it took the 8-bit from 8 to 19 tokens per second.
- **Every size passed** a four-step tool task, a 32,000-token recall test, 11 image questions, and loading in LM Studio.

The numbers are below. The scripts and raw results are in the [`tests`](https://huggingface.co/mlx-community/AREX-2-6bit/tree/main/tests) folder,
and on GitHub at [MuscleOtter/arex-2-mlx-tests](https://github.com/MuscleOtter/arex-2-mlx-tests).

<details>
<summary>AREX-2 compared with plain Qwen3.8-27B</summary>

| | AREX-2 | Qwen3.8-27B |
|---|---|---|
| Tokens used, all tests | 113,795 | 212,514 |
| Time, all tests | 249 min | 451 min |
| Easy tasks passed | 35 of 36 | 30 of 36 |
| Hard problems, first try | 15 of 24 | 11 of 24 |
| Hard problems, within 3 tries | 23 of 24 | 20 of 24 |

- **Same conditions for both:** 8-bit MLX, the same prompts, settings and 4,000-token limit, two runs of each test.
- **The gap is mostly length.** Every failed attempt by plain Qwen3.8-27B ran into the 4,000-token limit (31 of 31), against 9 of 13 for AREX-2. With a higher limit it might solve as many, more slowly.
- **Both ran with thinking on,** the default for both models.
- **With thinking off, in a real harness, they were level.** In MiniMax Code both passed 6 of 6 fix-the-tests trials, in 17 and 18 minutes. The efficiency gap above comes from thinking.
- **This is a small test on one Mac, not a benchmark.** It does not measure the long multi-round tasks AREX-2 was trained for.

</details>

<details>
<summary>Speed with a draft model</summary>

A draft model is a small helper that guesses ahead so the main model can write faster. It changes speed, not quality.
The helper made for plain Qwen3.8-27B, [incoai/Qwen3.8-27B-DFlash2](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2),
works with AREX-2 unchanged. Measured with [mlx-dspark](https://pypi.org/project/mlx-dspark/) 0.20.1, six prompts each:

| Size | Tokens/s without helper | Tokens/s with helper |
|---|---|---|
| 4-bit | 14 | 27 |
| 5-bit | 12 | 20 |
| 6-bit | 10 | 19 |
| 8-bit | 8 | 19 |

</details>

<details>
<summary>The test problems, by name</summary>

**Easy tasks (18):** merge intervals, integer to Roman numeral, longest palindromic substring, reverse Polish notation,
spiral matrix order, minimum window substring, decode nested string, next permutation, top-k frequent words,
simplify Unix path, expression calculator, count islands, edit distance, largest rectangle in a histogram,
trapping rain water, word break, course schedule order, longest increasing subsequence.

**Hard problems (12):** regular expression matching, text justification, strong password checker, valid number,
number to English words, skyline, shortest palindrome (200,000 characters), count smaller numbers after self
(100,000 elements), sliding window median (100,000 elements), burst balloons, trapping rain water in 2D,
max points on a line.

Each is one Python function checked by hidden tests. These are well-known problems, so both models have probably seen
them in training.

</details>

<details>
<summary>What was and was not checked</summary>

Every size passed all of these:

- A plain answer, with thinking on and off.
- A four-step task using tools, on 3 of 3 runs.
- Finding three facts hidden in a 32,000-token prompt.
- 11 questions about images: an invoice, a bar chart, counting shapes, two images at once, and fine print on a large image.
- Loading and chatting in LM Studio 0.4.8, with text, tool calls and images (checked on the 5-bit, including a copy downloaded back from this page).

The image questions were run at temperature 0. At the recommended settings the model read an invoice total correctly
in 6 of 7 tries; once it misread a digit and then corrected itself.

Not checked: video, prompts longer than 32,000 tokens, Macs with less than 64 GB, or BAAI's own benchmarks.

</details>

<details>
<summary>For developers, and how it was made</summary>

- **Tool calls** come back as `<tool_call><function=name><parameter=key>value</parameter></function></tool_call>`, not JSON. LM Studio converts them to standard tool calls for you.
- **Text only:** the model also loads in mlx-lm.
- **Conversion:** mlx-vlm 0.7.4, plain quantization, 6.66 bits per weight, original chat template unchanged.

```bash
python -m mlx_vlm convert --hf-path BAAI/AREX-2 --mlx-path AREX-2-6bit -q --q-bits 6
```

</details>

<details>
<summary>Common questions</summary>

- **Can AREX-2 run on a Mac?** Yes. These MLX builds run on Apple Silicon Macs. They were tested on an M4 Pro with 64 GB.
- **How much memory does AREX-2 need on a Mac?** On the test Mac the 5-bit used about 20 to 28 GB, the 6-bit 23 to 31 GB and the 8-bit 30 to 38 GB. That suggests a Mac with 32 GB or more, though nothing was run on a smaller one.
- **Which AREX-2 MLX size is best?** The tests here could not separate the 5-bit, 6-bit and 8-bit. The 5-bit needs the least memory of the three; the 8-bit is closest to the original.
- **Does AREX-2 work in LM Studio?** Yes, including images and tool calls.
- **Does it work in Ollama?** Not this build. Ollama uses the GGUF format, so use a GGUF version of AREX-2 there. Other MLX apps such as Jan and Msty may work but were not tested.
- **Can it read images?** Yes. Image input was kept in the conversion.
- **Is AREX-2 better than Qwen3.8-27B?** In a small local test it solved a few more problems and used about 46% fewer tokens. That is not a benchmark.

</details>

## Interested in a further distilled 4-bit?

The 4-bit here is a plain conversion, and it is the weakest size. A further distilled 4-bit might do better: the small
build is trained to copy the 8-bit's answers, which can win back some of the quality lost at this size. It would stay
the same size and keep image input. It takes a few days of computer time and may not close the gap, so I will only make
it if people want it. If you are interested, leave a comment in the
[Community tab](https://huggingface.co/mlx-community/AREX-2-4bit/discussions) and tell me what Mac you have.

## Questions and license

Found a problem or have a question? Open a discussion on the Community tab of this page.

Apache 2.0, the same as the original. Credit for the model goes to BAAI ([paper](https://arxiv.org/abs/2609.38288)).
