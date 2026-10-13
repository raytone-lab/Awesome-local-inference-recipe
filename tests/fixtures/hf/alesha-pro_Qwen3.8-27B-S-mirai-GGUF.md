---
license: apache-2.0
base_model: trymirai/Qwen3.8-27B-S-experimental
base_model_relation: quantized
pipeline_tag: text-generation
tags:
  - gguf
  - llama.cpp
  - mirai
  - 2-bit
  - qwen3.8
  - abliterated
  - control-vector
---

# Qwen3.8-27B, Mirai S, GGUF for llama.cpp

A GGUF of [Mirai's 2.4-bit Qwen3.8-27B](https://huggingface.co/trymirai/Qwen3.8-27B-S-experimental). Mirai's
compressed trellis codes are copied into the GGUF bit for bit, nothing is re-quantized. A 27B model in 11.2 GB that
runs on one 12 GB GPU, with tools, reasoning, images, and an optional file that removes refusals.

The format adds 4 ggml types, so mainline llama.cpp, LM Studio and Ollama will not load this file. 2 engines do. This
is a community conversion, not an official Mirai release.

## Which engine

| | [mirai-s-ada](https://github.com/professorpalmer/mirai-s-ada) | [llama.cpp-mirai-s](https://github.com/alesha-pro/llama.cpp-mirai-s) |
|---|---|---|
| | recommended | reference fork, the fallback |
| by | Cary Palmer | me |
| context on a 12 GB card | 262,144 with q8_0 KV | 128K with q4_0 KV, 74K with q8_0 |
| how | 51K to 58K positions of the cache in VRAM, the rest in system RAM | the cache is in VRAM |
| MTP drafting on 12 GB | yes | no, it needs 16 GB |
| decode, fresh chat | 76.6 tok/s on an RTX 4070 | 40 tok/s on an RTX 3090 |
| decode at 60K | 61.7 tok/s on the 4070 | 34.6 tok/s at 62K on the 3090 |
| platforms | Windows bundle, Linux from source | Linux from source |
| control vector in projection mode (the refusal vector) | yes | yes |

Use mirai-s-ada. It took the codec from my fork, checked that its greedy output matches the fork token for token, and
added what a 12 GB card needs: a KV cache that continues in system RAM, MTP drafting from the draft block inside this
GGUF, and fixes for apps that send `effort: "high"` or tiny output caps. The numbers in its column are Cary's, from his
RTX 4070 12 GB. I repeated them on Ubuntu with a 3090, see "Measured".

My fork is the fallback. This GGUF was made and verified on it, it changes rarely, and it will keep loading this file
if the other project moves or breaks. It is also the smaller diff if you want to read how the format works.

## Files

| File | Size | What |
|---|---:|---|
| `Qwen3.8-27B-S-mirai.gguf` | 11.2 GB | the model plus its MTP block (Q8_0). The token embedding (F16, 2.5 GB) stays in system RAM, 7.8 GB go to the GPU |
| `mmproj-Qwen3.8-27B-base-f16.gguf` | 0.93 GB | vision encoder taken from the base [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B). Mirai's checkpoint ships the language model only |
| `Qwen3.8-27B-S-mirai-refusal-direction.gguf` | 1.3 MB | optional: the refusal direction of this model as a llama.cpp control vector. See "Removing refusals" |

## Run it with mirai-s-ada

Windows: download the bundle from its [releases](https://github.com/professorpalmer/mirai-s-ada/releases), put the GGUF
in `models\` and run `start-server.ps1`. The launcher reads free VRAM and decides how much of the cache stays on the
card. Its README has an optional 2 minute step that makes a copy of the GGUF with the MTP block in Q4_0, which frees
VRAM for about 6K more positions.

Linux (I checked Ubuntu 22.04 with an RTX 3090, CUDA 12.8):

```bash
git clone --recurse-submodules https://github.com/professorpalmer/mirai-s-ada && cd mirai-s-ada
cmake -S engine -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON -DLLAMA_CURL=OFF \
  -DCUDAToolkit_ROOT=/usr/local/cuda -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc -DCMAKE_CUDA_ARCHITECTURES=86
cmake --build build -j --target llama-server
hf download alesha-pro/Qwen3.8-27B-S-mirai-GGUF --local-dir models
MIRAI_KV_VRAM_CELLS=44000 ./start-server.sh
```

`CMAKE_CUDA_ARCHITECTURES` is your GPU generation: 86 for RTX 30, 89 for RTX 40. `MIRAI_KV_VRAM_CELLS` is how many
positions of the cache stay in VRAM: 44,000 is what I ran on a 3090 held to 12 GB, a bigger card can take more. The
Linux launcher does not size this for you. The server listens on `http://127.0.0.1:8080/v1`. For images add
`MIRAI_MMPROJ=models/mmproj-Qwen3.8-27B-base-f16.gguf` in front (the encoder runs on the CPU and takes no VRAM).

## Run it with the reference fork

```bash
git clone https://github.com/alesha-pro/llama.cpp-mirai-s && cd llama.cpp-mirai-s
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=86 \
  -DCUDAToolkit_ROOT=/usr/local/cuda -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc
cmake --build build -j --target llama-server
hf download alesha-pro/Qwen3.8-27B-S-mirai-GGUF --local-dir qwen3.8-s
```

Link against CUDA 12 cuBLASLt (`-DCUDAToolkit_ROOT`): with cuBLAS 11 the int8 GEMM falls back to a tile that is
about half as fast. For other GPUs set `CMAKE_CUDA_ARCHITECTURES` accordingly.

```bash
# 12 GB card, 128K context (q4_0 KV cache)
./build/bin/llama-server -m qwen3.8-s/Qwen3.8-27B-S-mirai.gguf -ngl 99 -fa on -np 1 --jinja \
  -c 131072 -ctk q4_0 -ctv q4_0 -b 1024 -ub 1024

# 12 GB card, 74K context with the more accurate q8_0 KV cache
./build/bin/llama-server -m qwen3.8-s/Qwen3.8-27B-S-mirai.gguf -ngl 99 -fa on -np 1 --jinja \
  -c 73728 -ctk q8_0 -ctv q8_0 -b 1024 -ub 1024

# 16 GB card, 128K context with MTP speculative decoding
./build/bin/llama-server -m qwen3.8-s/Qwen3.8-27B-S-mirai.gguf -ngl 99 -fa on -np 1 --jinja \
  -c 131072 -ctk q8_0 -ctv q8_0 --spec-type draft-mtp --spec-draft-n-max 3

# images, encoder on the CPU (0 VRAM): add to any line above
  --mmproj qwen3.8-s/mmproj-Qwen3.8-27B-base-f16.gguf --no-mmproj-offload -t <physical cores>
```

`-np 1` matters on this hybrid model: every server slot keeps its own DeltaNet state, and the default slot count
adds about 450 MB (11.7 GB instead of 11.3 GB at 128K), which leaves a 12 GB card almost nothing.

Thinking is on by default (Qwen3.8 chat template). The server accepts `reasoning_effort` (`low`, `medium`, `xhigh`)
and `chat_template_kwargs: {"enable_thinking": false}`.

## Removing refusals (optional)

The weights here are trellis codes, so the usual abliteration (editing the matrices) cannot be written back. I
measured the refusal direction on this quantized model and put it in a control vector file. The engine subtracts it
from the residual stream after every layer while the model runs: `h -= (h.v) v`. Without the file nothing changes.

Add 2 arguments to the `llama-server` line:

```bash
--control-vector-scaled Qwen3.8-27B-S-mirai-refusal-direction.gguf:1.0 --cvec-mode project
```

Both engines take them. mirai-s-ada documents the mode in
[docs/CONTROL-VECTOR.md](https://github.com/professorpalmer/mirai-s-ada/blob/main/docs/CONTROL-VECTOR.md): off by
default, with the same numbers as below. They are my measurements, and Cary has not run his long suite or HumanEval
with the vector on. With its Linux launcher it is one variable:

```bash
MIRAI_CVEC=models/Qwen3.8-27B-S-mirai-refusal-direction.gguf MIRAI_KV_VRAM_CELLS=44000 ./start-server.sh
```

A refusal is counted by a regex on the start of the answer. One RTX 3090:

| | without the vector | with the vector |
|---|---:|---:|
| mirai-s-ada: 64 harmful instructions (AdvBench, not used for the direction), thinking off | 64 refused | 0 |
| mirai-s-ada: 82 held-out behaviours (JailbreakBench, non-AdvBench rows), thinking off | 78 | 0 |
| mirai-s-ada: 24 harmful instructions, thinking on | 23 | 1 |
| mirai-s-ada: 10-prompt probe, sampled, thinking off / on | 10 / 8 | 0 / 0 |
| reference fork: 64 harmful instructions, thinking off | 63 | 0 |
| reference fork: 82 held-out behaviours, thinking off | not run | 0 |
| reference fork: 24 harmful instructions, thinking on | 23 | 0 |
| either engine: 32 ordinary instructions refused | 0 | 0 |

What it costs on ordinary text: KL to the model without the vector is 0.019 on prose and 0.009 on code, and the top
token stays the same in 94.0% and 97.1% of positions. Decode speed is the same (69.7 against 69.9 tok/s on mirai-s-ada,
39.2 against 39.9 on the fork). 5 of 5 small agent coding tasks passed with it, 1 of them on a second run. Tool calls, reasoning effort and images
work with it.

How it was made: residual stream after every layer at the last prompt token, 256 AdvBench against 256 Alpaca
instructions, in 6 prompt contexts (thinking on and off, with and without a system message). Per layer I took the
difference of means, removed its component along the mean harmless state, normalized, and averaged the 6 contexts. The
file has one direction for each of layers 1 to 63. The tools are in the fork (`llama-resid-dump`,
`tools/mirai-s/refusal_direction.py`) and reproduce the file byte for byte.

The catch: the counts come from a regex over 10 to 82 prompts, I did not read the answers one by one. A very different
system prompt may leave more refusals. What the model writes with the vector on is your responsibility.

## Measured

mirai-s-ada, 262,144 window, q8_0 KV, MTP draft 2:

| | RTX 4070 12 GB, Windows (Cary's numbers) | RTX 3090 held to 12 GB, Ubuntu (mine) |
|---|---:|---:|
| cache positions in VRAM | about 58K, with the Q4_0 copy of the MTP block | 44,000, with this GGUF as published |
| VRAM | | 11.3 GB at load, 11.4 GB peak |
| decode, fresh chat or 8K | 76.6 tok/s | 66.9 tok/s at 8K |
| decode at 60K / 120K / 180K | 61.7 / 19.5 / 11.4 | 27.9 / 9.5 / 5.8 |
| prefill | 1,090 tok/s on a 16.8K prompt | 1,124 tok/s on an 8K prompt |
| greedy output against the reference fork | identical | identical on 5 of 5 prompts |

Past the positions kept in VRAM every step reads the rest of the cache from system RAM over PCIe, and decode slows
down. That is the difference at 60K: his run has 60K inside VRAM, mine stops at 44K. With the same 44K to 45K in VRAM
his card did 40.3 tok/s at 60K against my 27.9. My 3090s are on PCIe 3.0. I think that is why, but I did not test it.

The reference fork, one RTX 3090 at 300 W:

| Setup | Peak VRAM | Decode, fresh chat | Decode at 62K | Prefill, 6.9K prompt |
|---|---:|---:|---:|---:|
| 12 GB: 128K, q4_0 KV, `-ub 1024` | 11.3 GB | 39.7 tok/s | 34.6 tok/s | 1008 tok/s |
| 12 GB: 74K, q8_0 KV, `-ub 1024` | 11.1 GB | 40.0 tok/s | 34.9 tok/s | 1009 tok/s |
| 16 GB: 128K, q8_0 KV, MTP 3 | 14.6 GB | 85 code / 57 prose | | 806 tok/s |

Decode at 117K with the 128K q4_0 setup: 30.4 tok/s. With `-b 512 -ub 512` the fork fits 147K at q4_0 (11.4 GB peak)
or 82K at q8_0 (11.2 GB). VRAM is what a 12 or 16 GB card needs; speeds on smaller cards will be lower than on a 3090.
Mirai's own vLLM plugin on the same card is faster than the fork on short prompts (44 vs 39 tok/s decode, 1336 vs 1120
prefill, 107 vs 84 on code with MTP at 300 W) but fits less context in 12 GB (37.6K with bf16 KV, 74.4K with fp8 KV).

Images with the encoder on the CPU (48-core EPYC, `-t 47`): a 1280x800 screenshot takes about 7 s to encode, a
2600x2400 image about 44 s. On the GPU the encoder adds 0.8 GB of VRAM (1.3 GB at peak) and a screenshot takes about 1.5 s.

## Verification

- The converter's reference decoder matches Mirai's own decode of the same rows to 3e-8; the CUDA kernels match the
  CPU reference in `test-backend-ops`.
- Greedy output against Mirai's vLLM plugin, 10 prompts (2 of them ~7K tokens), 64 tokens: 8 identical token for
  token; the other 2 split later on near ties (the one I checked: top two candidates 0.0007 logprob apart). Top-5
  logprobs at the first token overlap 5 of 5 on all 10.
- `test-backend-ops` also covers the flash attention and gated delta net paths the fork changes for long context.
- mirai-s-ada on Ubuntu against the fork's greedy dumps: identical on 5 of 5 prompts with thinking off. With thinking
  on, the 300-token dump is a prefix of its output in 5 of 5.

## Credits

The codec, the compressed weights and the vLLM plugin whose CUDA kernels the fork ports are by
[Mirai Labs](https://x.com/trymirai). The base model and the vision encoder are Qwen's. The runtime is
[llama.cpp](https://github.com/ggml-org/llama.cpp) (MIT). [mirai-s-ada](https://github.com/professorpalmer/mirai-s-ada),
the 262K serve, is by Cary Palmer on top of PrismML's llama.cpp fork. This repo is under Apache-2.0, like Mirai's
checkpoint; the license text is in `LICENSE`.
