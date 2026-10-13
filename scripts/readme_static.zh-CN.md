# 本地推理配方精选 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](README.md) | **简体中文**

> 模型 × 引擎 × 硬件 → 实测速度与成本，每个数字都链接到来源。聚焦消费级与二手硬件，预算 3 万美元以内。

<sub>暂定名：**RecipeBench** · 共 {{N}} 条配方（文字 {{NT}} · 图像 {{NI}} · 影音 {{NV}}）· 数据截至 2026-10-13 · <a href="explore.html">配方库</a> · <a href="submit.html">提交配方</a></sub>

## 目录

{{TOC}}

## 图例

| 来源等级 | 含义 | 格式 |
|---|---|---|
| 🏛️ **官方** | 项目方或厂商发布的数字 | **模型** · 引擎 `量化` — 硬件 → **关键数字** 等级 [来源] |
| ✅ **实测** | 作者本人跑出，附日志或截图 | **tok/s** 指单路生成速度（不含读入，不含多路合计） |
| 🔁 **转述** | 二手引用，请回原帖核对 | 预算档按公开的最低硬件价格（美元）划分 |
| 📣 **宣称** | 预测值，无复现条件 | 未知字段一律不估算，显示「未见公开数据」 |
<!--RECIPES-->

## 引擎与工具

<!--ENGINES-->

## 相关榜单与清单

<!--RELATED-->

## 参与贡献

一条配方一个 PR。从 [提交页](submit.html) 复制 YAML 模板，只填来源里写明的内容（其余写 `null`），运行 `node scripts/validate.mjs` 校验并附上原帖链接。然后运行 `python3 scripts/gen_readme.py` 重新生成两份 README。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

本地开发：`python3 -m http.server 5190` → `index.html`（首页）· `explore.html`（筛选、排序、散点图）· 数据格式见 [`schema/recipe.schema.json`](schema/recipe.schema.json)。

<details><summary>网站预览</summary>

<img src="docs/screenshot.png" width="760" alt="RecipeBench">

</details>

## 许可证

- 代码：[MIT](LICENSE)
- 数据（`data/`）：[CC BY 4.0](LICENSE-DATA)。可自由使用，需署名 RecipeBench 并保留每条配方的原始来源链接。
