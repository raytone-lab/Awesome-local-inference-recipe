# Awesome Local Inference Recipes [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

> Model × engine × hardware → measured speed and cost, with every number linked to its source. Consumer and used hardware, up to $30k.

<sub>{{N}} recipes ({{NT}} text · {{NI}} image · {{NV}} video/audio) · data as of 2026-10-13 · <a href="explore.html">Explorer</a> · <a href="submit.html">Submit</a></sub>

<sub>Site links point to GitHub Pages; if it is not live yet, clone the repo and open <code>explore.html</code> locally (<code>python3 -m http.server</code>).</sub>

**New:** step-by-step [recipe guides](recipes/README.md) · [Getting started](docs/getting-started.md)

## Contents

{{TOC}}

## Legend

| Source level | Meaning | Format |
|---|---|---|
| 🏛️ **Official** | vendor or project number | **Model** · Engine `quant` — Hardware → **key number** level \[source\] |
| ✅ **Measured** | author ran it, with log or screenshot | **tok/s** = single-stream generation (not prefill, not aggregate) |
| 🔁 **Relayed** | second-hand, verify upstream | Tiers use the lowest published hardware price (USD) |
| 📣 **Claimed** | projection, no reproduction | Unknown values are never estimated |
<!--RECIPES-->

## Engines & Tools

<!--ENGINES-->

## Related Lists & Benchmarks

<!--RELATED-->

## Contributing

One recipe = one PR. Copy the YAML template from [submit.html](submit.html), fill only what the source shows (`null` otherwise), run `node scripts/validate.mjs`, and link the post. Then run `python3 scripts/gen_readme.py` to regenerate all READMEs. See [CONTRIBUTING.md](CONTRIBUTING.md).

Dev: `python3 -m http.server 5190` → `index.html` (landing) · `explore.html` (filter/sort/scatter) · schema in [`schema/recipe.schema.json`](schema/recipe.schema.json).

<details><summary>Site preview</summary>

<img src="docs/screenshot.png" width="760" alt="Awesome Local Inference Recipes">

</details>

## License

- Code: [MIT](LICENSE)
- Data (`data/`): [CC BY 4.0](LICENSE-DATA). Reuse it freely with attribution to Awesome Local Inference Recipes and the original sources linked in each recipe.
