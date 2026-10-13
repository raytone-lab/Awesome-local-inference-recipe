# Infer Recipes（本地推理配方聚合 · 原型）
跨引擎、跨硬件的本地推理“配方”库：模型 × 量化 × 引擎 × 硬件 → 速度 / 成本 / 上下文 / 来源等级。聚焦 3 万美元以内方案。

- 数据：`data/recipes.json`（160 条，来自 2026-10 的报告整理），价格快照 `data/prices.json`
- Schema：`schema/recipe.schema.json`；校验：`node scripts/validate.mjs`
- 运行：纯静态，`python3 -m http.server 5190 --bind 127.0.0.1` 后打开 http://127.0.0.1:5190
- 功能：搜索、类别/引擎/硬件族/来源等级筛选、预算滑杆、可排序表格、详情抽屉、$/tok/s 计算列、tok/s–成本散点图、提交页
- `scripts/convert.py`：从原始报告行一次性转换（未知值一律 null，不估算）

## 已知限制
- 所有 launch_command 目前为空；引擎多为关键词推断（62 条“其他/未注明”）
- 成本仅在来源给出单一美元数时填入（取区间下限）；“按张计价”的多卡行未折算
- date 字段大多为空；只有文字模型有 tok/s 数值
