# ローカル推論レシピ集 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

> モデル × エンジン × ハードウェア → 実測の速度とコスト。すべての数字に出典リンクを付けています。対象はコンシューマー機と中古ハードウェア、予算 3 万ドルまで。

<sub>レシピ {{N}} 件（テキスト {{NT}} · 画像 {{NI}} · 動画・音声 {{NV}}）· 2026-10-13 時点のデータ · <a href="explore.html">エクスプローラー</a> · <a href="submit.html">レシピを投稿</a></sub>

<sub>サイトへのリンクは GitHub Pages を指しています。表示されない場合は、リポジトリをクローンしてローカルで <code>explore.html</code> を開いてください（<code>python3 -m http.server</code>）。</sub>

**新着：** 手順付きの[レシピガイド](recipes/README.md)（英語）· [はじめに](docs/getting-started.md)（英語）

> 各レシピのモデル名・ハードウェア・数値は元の投稿から引用しています。日本語訳のない説明文は「出典を参照」と表示します。

## 目次

{{TOC}}

## 凡例

| 出典レベル | 意味 | 表記 |
|---|---|---|
| 🏛️ **公式** | 開発元やベンダーが公表した数字 | **モデル** · エンジン `量子化` — ハードウェア → **主要な数字** レベル \[出典\] |
| ✅ **実測** | 投稿者本人が計測（ログやスクリーンショットあり） | **tok/s** は 1 ストリームの生成速度（プリフィルや合計値は含まない） |
| 🔁 **伝聞** | 他人の結果の引用。元の投稿で確認を | 価格帯は公開されている最安のハードウェア価格（米ドル）で区分 |
| 📣 **主張** | 見込み値で、再現条件なし | 不明な値は推定しません |
<!--RECIPES-->

## エンジンとツール

<!--ENGINES-->

## 関連リスト・ベンチマーク

<!--RELATED-->

## コントリビュート

1 レシピにつき 1 PR でお願いします。[投稿ページ](submit.html)の YAML テンプレートをコピーし、出典に書かれている内容だけを埋めてください（それ以外は `null`）。`node scripts/validate.mjs` でチェックし、元の投稿へのリンクを添えてください。その後 `python3 scripts/gen_readme.py` で README をすべて再生成します。詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

ローカル開発：`python3 -m http.server 5190` → `index.html`（トップ）· `explore.html`（絞り込み・並べ替え・散布図）· スキーマは [`schema/recipe.schema.json`](schema/recipe.schema.json)。

<details><summary>サイトのプレビュー</summary>

<img src="docs/screenshot.png" width="760" alt="Awesome Local Inference Recipes">

</details>

## ライセンス

- コード：[MIT](LICENSE)
- データ（`data/`）：[CC BY 4.0](LICENSE-DATA)。Awesome Local Inference Recipes と、各レシピに記載された元の出典を明記すれば自由に再利用できます。
