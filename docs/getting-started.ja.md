# はじめに

[English](getting-started.md) | [简体中文](getting-started.zh-CN.md) | **日本語**

予算と手持ちのハードウェアに合わせてレシピを選び、実際に動かすまでの流れです。

## 1. 手持ちのハードウェアから選ぶ
| 手持ちの環境 | まず見るもの | よく使われるエンジン |
|---|---|---|
| Mac（Apple Silicon、ユニファイドメモリ 32 GB 以上） | Mac のレシピ。メモリが多いほど大きなモデルが動きます | MLX、oMLX、llama.cpp、mlx-serve |
| NVIDIA のコンシューマー GPU（RTX 3090/4090/5090 など） | 量子化後に VRAM に収まるモデル、またはオフロード前提の MoE モデル | llama.cpp、vLLM、SGLang、ExLlama、Strata |
| DGX Spark | 128 GB のユニファイドメモリ。大きな MoE モデル向き | vLLM、TensorFold、ExLlama |
| AMD（Strix Halo、Radeon） | Strix Halo ならユニファイドメモリで大きなモデルも動きます | llama.cpp（HIP/Vulkan）、Strata、Halogen |
| 中古データセンター GPU（V100 など） | VRAM 単価が安い。ドライバーと CUDA の対応状況に注意 | llama.cpp、Strata |

これからハードを買うなら、[README](../README.ja.md) の価格帯（2,500 / 7,000 / 14,000 / 30,000 ドルまで）を参考にしてください。

## 2. レシピの読み方
各行は「モデル × エンジン × ハードウェア → 数値」です。まず**出典レベル**を確認しましょう。✅ 実測と 🏛️ 公式は、🔁 伝聞や 📣 主張より信頼できます。[エクスプローラー](https://raytone-lab.github.io/Awesome-local-inference-recipe/explore.html)では、ハードウェア、モデルファミリー、エンジン、タグ（`4bit`、`MoE` など）で絞り込めます。

## 3. 動かしてみる
1. [ガイドページ](../recipes/README.ja.md)があればそれを、なければ出典のリンクを開きます。
2. レシピに書かれたモデルファイルと量子化をそのままダウンロードします（多くは Hugging Face）。
3. レシピにあるエンジンのバージョンをインストールします。フォーク版を使う場合は明記してあります。
4. 起動コマンドは出典どおりに。「未公開」となっている場合は元の投稿に従い、フラグを推測で足さないでください。
5. 速度を比べるときは、コンテキスト長とプロンプト長を出典と揃えてください。

## 4. 結果を共有する
レシピ投稿用の issue か PR をお送りください。詳しくは [CONTRIBUTING](../CONTRIBUTING.md) を参照してください。
