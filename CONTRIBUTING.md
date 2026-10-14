# Contributing / 贡献指南

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) first. · [中文](#中文) · [日本語](#日本語)

## Add a recipe
1. Easiest: open a **[Recipe submission](../../issues/new?template=recipe.yml)** issue. Or fork → branch → append to `data/recipes.json` (fields: `schema/recipe.schema.json`, template: `submit.html`).
2. `node scripts/validate.mjs` must pass (CI runs it on every PR).
3. Regenerate READMEs: `python3 scripts/gen_readme.py`.
4. Link the original source; for your own runs include the command and output.
5. No estimates, no invented values: unknown → `null`. Link and summarize, don't copy posts.
6. Source level: official / measured / relayed / claimed (see [docs/sources.md](docs/sources.md)).

## 中文
1. 最简单：提一个「Recipe submission」issue；或 Fork 后在 `data/recipes.json` 追加记录。
2. `node scripts/validate.mjs` 必须通过（PR 会自动跑 CI）。
3. 运行 `python3 scripts/gen_readme.py` 重新生成两份 README。
4. 附原始来源链接；自测请附命令与输出。
5. 不估算、不编造，未知写 `null`；只留链接与摘要。
6. 来源等级：官方 / 实测 / 转述 / 宣称，详见 [docs/sources.md](docs/sources.md)。

Maintainers: Hugging Face candidate ingestion is described in [docs/sources.md](docs/sources.md).

## 日本語
1. いちばん簡単なのは「Recipe submission」の issue を立てることです。または Fork して `data/recipes.json` に追記してください。
2. `node scripts/validate.mjs` が通ること（PR では CI が自動で実行します）。
3. `python3 scripts/gen_readme.py` で README を再生成してください。
4. 元の出典へのリンクを付けてください。自分で計測した場合はコマンドと出力も。
5. 推定や創作はしないでください。不明な値は `null` に。投稿の全文転載はせず、リンクと要約だけにします。
6. 出典レベル：公式 / 実測 / 伝聞 / 主張（[docs/sources.md](docs/sources.md) を参照）。
