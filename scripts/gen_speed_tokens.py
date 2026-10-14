#!/usr/bin/env python3
"""Precompute real token boundaries for speed.html (writes data/speed-tokens.json).
Uses the Qwen3 tokenizer (Hugging Face `Qwen/Qwen3-8B`, tokenizer.json only). Needs: pip install tokenizers
Each token is the exact slice of the source text covered by that token's offsets; byte-level tokens that
split a multi-byte character yield '' (they still count as one token, like a real stream).
Run: python3 scripts/gen_speed_tokens.py"""
import json
from pathlib import Path
from tokenizers import Tokenizer
R = Path(__file__).resolve().parent.parent
TOK = 'Qwen/Qwen3-8B'
TEXT = {
'en': """Running a large language model locally comes down to three numbers: how much memory you have, how fast that memory is, and how well your inference engine uses it.

Generation speed is mostly limited by memory bandwidth. Every new token requires reading the active weights once, so a 4-bit 27B dense model moves roughly 14 GB per token. On a GPU with 1 TB/s of bandwidth, that caps you near 70 tokens per second before any tricks.

Mixture-of-experts models change the math. Only a few experts are active for each token, so a 125B MoE with 10B active parameters can generate faster than a much smaller dense model, as long as the full weights fit in memory or can be streamed from system RAM.

Speculative decoding adds another multiplier. A small draft model, or extra MTP heads, guesses several tokens ahead, and the big model verifies them in one pass. When the guesses are accepted, you get two or three tokens for the price of one.

Finally, prompt processing (prefill) is compute-bound, not bandwidth-bound. That is why a Mac can feel quick when chatting but slow when you paste a long document, while a discrete GPU stays fast in both cases.""",
'zh-CN': """在本地运行大语言模型，归根结底取决于三个数字：你有多少内存、内存有多快，以及推理引擎能把它用得多好。

生成速度主要受内存带宽限制。每生成一个新 token，都要把激活的权重完整读一遍。一个 4-bit 量化的 27B 稠密模型，每个 token 大约要搬运 14 GB 数据。在带宽 1 TB/s 的显卡上，不靠任何技巧，速度上限大约是每秒 70 个 token。

混合专家（MoE）模型改变了这个算法。每个 token 只激活少数几个专家，所以一个总参数 125B、激活 10B 的 MoE 模型，只要权重放得进内存，或者能从系统内存流式读取，生成速度反而可能比小得多的稠密模型更快。

投机解码又加了一个倍数。用一个小的草稿模型或额外的 MTP 头先猜后面几个 token，再由大模型一次性验证。猜中的时候，一次计算就能得到两三个 token。

最后，提示词处理（预填充）受算力限制，而不是带宽。这就是为什么 Mac 聊天时感觉很快，但粘贴一篇长文档时会变慢，而独立显卡在两种情况下都很快。""",
'ja': """大規模言語モデルをローカルで動かすとき、決め手になるのは三つの数字です。メモリがどれだけあるか、そのメモリがどれだけ速いか、そして推論エンジンがそれをどれだけうまく使えるか。

生成速度はほぼメモリ帯域で決まります。新しいトークンを一つ出すたびに、アクティブな重みを一度読み込む必要があるからです。4 ビット量子化した 27B の密なモデルなら、1 トークンあたり約 14 GB を読み出します。帯域 1 TB/s の GPU では、工夫なしだと毎秒 70 トークン前後が上限です。

Mixture-of-Experts（MoE）モデルでは事情が変わります。トークンごとに動くのは一部のエキスパートだけなので、総パラメータ 125B・アクティブ 10B の MoE は、重みがメモリに収まるかシステム RAM からストリーミングできれば、ずっと小さな密モデルより速く生成できることがあります。

投機的デコードはさらに倍率を上げます。小さなドラフトモデルや追加の MTP ヘッドが数トークン先を予想し、大きなモデルが一度にまとめて検証します。予想が当たれば、1 回の計算で 2〜3 トークンが手に入ります。

最後に、プロンプト処理（プリフィル）は帯域ではなく計算量で決まります。Mac がチャットでは速く感じるのに長い文書を貼ると遅くなり、単体 GPU はどちらでも速いのはこのためです。""",
}
t = Tokenizer.from_pretrained(TOK)
out = {'tokenizer': TOK, 'note': 'token strings are exact source-text slices from tokenizer offsets', 'texts': {}}
for lang, s in TEXT.items():
    enc = t.encode(s, add_special_tokens=False); toks = []; pos = 0
    for a, b in enc.offsets:
        if b <= pos: toks.append(''); continue
        toks.append(s[pos:b]); pos = b
    if pos < len(s): toks[-1] += s[pos:]
    assert ''.join(toks) == s, lang
    out['texts'][lang] = toks
    print(lang, len(toks), 'tokens')
(R/'data/speed-tokens.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n')
