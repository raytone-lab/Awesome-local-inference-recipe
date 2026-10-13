# 贡献指南
1. Fork → 新分支 → 在 `data/recipes.json` 追加记录（字段见 `schema/recipe.schema.json`，模板见 submit.html）
2. `node scripts/validate.mjs` 必须通过
3. PR 描述附来源链接；自测附命令与输出
4. 不估算、不编造：未知写 null。不搬运帖子全文，只留链接与摘要
5. 来源等级：官方 / 实测 / 转述 / 宣称

## 自动候选（Hugging Face）/ Auto candidates
维护者每周运行 `python3 scripts/ingest_hf.py`，再用 `python3 scripts/review_candidates.py` 人工审核；只有 approve 后才进入 `data/recipes.json`。详见 `docs/sources.md`。
