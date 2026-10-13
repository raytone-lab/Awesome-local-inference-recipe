# Awesome Local Inference Recipes [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Model × engine × hardware → measured speed and cost, with every number linked to its source. Consumer and used hardware, ≤ $30k.
> 本地推理配方：跨引擎、消费级/二手硬件、每个数字标来源。

<sub>Working name: **RecipeBench** (placeholder) · {{N}} recipes ({{NT}} text · {{NI}} image · {{NV}} video/audio) · data as of 2026-10-13 · <a href="explore.html">Explorer</a> · <a href="submit.html">Submit</a></sub>

## Contents

{{TOC}}

## Legend

| Source level | | Format |
|---|---|---|
| 🏛️ **官方** Official | vendor/project number | `Model · Engine` `quant` — Hardware → **key number** level [source] |
| ✅ **实测** Measured | author ran it, log/screenshot | **tok/s** = single-stream generation (not prefill, not aggregate) |
| 🔁 **转述** Relayed | second-hand, verify upstream | Tiers use the lowest published hardware price (USD) |
| 📣 **宣称** Claimed | projection, no repro | Unknown fields are never estimated (未见公开数据) |
<!--RECIPES-->

## Engines & Tools

<!--ENGINES-->

## Related Lists & Benchmarks

<!--RELATED-->

## Contributing

<details><summary>Site preview</summary>

<img src="docs/screenshot.png" width="760" alt="RecipeBench">

</details>


One recipe = one PR. Copy the YAML template from [submit.html](submit.html), fill only what the source shows (`null` otherwise), run `node scripts/validate.mjs`, and link the post. Then run `python3 scripts/gen_readme.py` to regenerate this file. See [CONTRIBUTING.md](CONTRIBUTING.md).

Dev: `python3 -m http.server 5190` → `index.html` (landing) · `explore.html` (filter/sort/scatter) · schema in [`schema/recipe.schema.json`](schema/recipe.schema.json).

## License

- Code: [MIT](LICENSE)
- Data (`data/`): [CC BY 4.0](LICENSE-DATA). Reuse it freely with attribution to RecipeBench and the original sources linked in each recipe.
