#!/usr/bin/env python3
"""Generate how-to guide pages (recipes/<id>.md + recipes/<id>.zh-CN.md) for a curated batch.
Only uses fields in data/recipes.json; never invents commands or numbers.
Run: python3 scripts/gen_recipe_pages.py"""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = {r['id']: r for r in json.load(open(R/'data/recipes.json'))}
GUIDES = [  # curated first batch: spans Mac / NVIDIA / DGX Spark / AMD / used datacenter / image / video
 'hf-ddalcu-qwen3-8-flash-next-mlx-serve-mixed-4-8bit-1','hf-youssofal-qwen3-6-27b-mtplx-optimized-speed-1',
 'hf-prism-ml-ternary-bonsai-2-27b-gguf-5','hf-prism-ml-ternary-bonsai-2-27b-gguf-1','hf-byteshape-qwen3-8-27b-gguf-1',
 'hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1','x-004','text-022','x-001','x-009','x-007','text-018',
 'image-001','video-audio-001']
ENGINE_URL = {
 'llama.cpp':'https://github.com/ggml-org/llama.cpp','MLX':'https://github.com/ml-explore/mlx-lm','vLLM':'https://github.com/vllm-project/vllm',
 'SGLang':'https://github.com/sgl-project/sglang','ExLlama':'https://github.com/turboderp-org/exllamav3','Strata':'https://github.com/Niko1221/Strata',
 'oMLX':'https://github.com/jundot/omlx','TensorFold':'https://github.com/ashhart/TensorFold','LightX2V':'https://github.com/ModelTC/LightX2V',
 'Halogen':'https://github.com/peonist-ai/halogen-flash-server','ComfyUI':'https://github.com/comfyanonymous/ComfyUI'}
LV = {'官方':('🏛️ Official','🏛️ 官方'),'实测':('✅ Measured','✅ 实测'),'转述':('🔁 Relayed','🔁 转述'),'宣称':('📣 Claimed','📣 宣称')}
HWF = {'NVIDIA 消费级':'NVIDIA consumer','二手数据中心卡':'Used datacenter GPU','其他':'Other'}
CJK = re.compile(r'[\u3400-\u9fff\uff00-\uffef\u3000-\u303f]')
def en(s):
    if not s: return None
    s = re.sub(r'（[^）]*）|\([^)]*[\u3400-\u9fff][^)]*\)', '', str(s))
    s = ' '.join(w for w in s.split() if not CJK.search(w)).strip(' ;,·')
    return s or None
def hf_repo(r):
    m = re.match(r'https://huggingface\.co/([^/]+/[^/?#]+)', r['source_url'])
    return m.group(1) if m else None
def engine_url(e):
    if not e: return None
    for k, u in ENGINE_URL.items():
        if e == k or e.startswith(k+' '): return u
def page(r, lang):
    Z = lang == 'zh'; T = (lambda s: s) if Z else en
    lvl = LV.get(r['source_level'], ('',''))[1 if Z else 0]
    na = '未公开，见来源' if Z else 'not published, see source'
    repo = hf_repo(r); eu = engine_url(r.get('engine'))
    if Z: metric = r.get('metric')
    else: metric = r.get('metric_en') or (f"{r['tok_s']} tok/s (generation)" if r.get('tok_s') else None)
    cmd = r.get('launch_command')
    if cmd and cmd.startswith('见'): cmd = None
    other = 'README.md' if not Z else 'README.zh-CN.md'
    L = []
    L.append(f"# {T(r['model']) or r['model']} · {T(r.get('engine')) or '—'} · {T(r['hardware']) or r['hardware']}")
    L.append('')
    L.append(f"[English]({r['id']}.md) | [简体中文]({r['id']}.zh-CN.md) · [← {'返回列表' if Z else 'All recipes'}](../{other})")
    L.append('')
    h = (lambda zh, e: zh if Z else e)
    L.append(f"> {h('来源等级','Source level')}: **{lvl}** · {h('日期','Date')}: {r.get('date') or '—'} · {h('数字均摘自来源，未经本仓库复测。','Numbers are quoted from the source and have not been re-run by this repo.')}")
    L.append('')
    L.append(f"## {h('硬件','Hardware')}\n")
    L.append(f"- {T(r['hardware']) or r['hardware']} ({r['hardware_family'] if Z else HWF.get(r['hardware_family'], r['hardware_family'])})")
    cost = r.get('hardware_cost_text') if Z else (f"≈ ${r['hardware_cost_usd']:,}" if r.get('hardware_cost_usd') else None)
    L.append(f"- {h('参考价格','Reference cost')}: {cost or na}\n")
    L.append(f"## {h('模型','Model')}\n")
    L.append(f"- {T(r['model']) or r['model']}" + (f" · `{T(r['quant'])}`" if T(r.get('quant')) else ''))
    L.append(f"- {h('下载','Download')}: " + (f"[huggingface.co/{repo}](https://huggingface.co/{repo})" if repo else na) + '\n')
    L.append(f"## {h('引擎','Engine')}\n")
    L.append(f"- {T(r.get('engine')) or na}" + (f" — {h('安装见','install:')} {eu}" if eu else ''))
    if r.get('engine_note') and T(r['engine_note']): L.append(f"- {h('备注','Note')}: {T(r['engine_note'])}")
    L.append('')
    L.append(f"## {h('启动命令','Launch command')}\n")
    if cmd and T(cmd):
        L.append(f"```bash\n{cmd if Z else T(cmd)}\n```")
        if '...' in cmd or '<' in cmd: L.append(f"\n{h('命令为来源中的节选（含 `...`/占位符），完整参数请看来源。','Excerpt from the source (contains `...`/placeholders); see the source for full arguments.')}")
    else: L.append(f"{h('命令未公开，请参考来源。','Command not published — see source.')}")
    L.append('')
    L.append(f"## {h('关键参数','Key parameters')}\n")
    L.append(f"- {h('上下文','Context')}: {T(r.get('context')) or '—'}")
    L.append(f"- {h('并发','Concurrency')}: {T(r.get('concurrency')) or '—'}")
    if r.get('tags'): L.append(f"- {h('标签','Tags')}: " + ', '.join(f'`{t}`' for t in r['tags']))
    L.append('')
    L.append(f"## {h('预期速度','Expected speed')}\n")
    L.append(f"- {metric or na} ({lvl})\n")
    L.append(f"## {h('注意事项','Caveats')}\n")
    cav = []
    if r['source_level'] in ('宣称','转述'): cav.append(h('非一手实测（宣称/转述），实际速度可能不同。','Not a first-hand measurement (claimed/relayed); your results may differ.'))
    if Z and r.get('source_note'): cav.append(r['source_note'].split('; 原文')[0][:200])
    cav.append(h('速度随驱动、引擎版本、上下文长度和提示长度变化。','Speed varies with drivers, engine version, context length and prompt length.'))
    L += [f'- {c}' for c in cav]; L.append('')
    L.append(f"## {h('来源与致谢','Source & attribution')}\n")
    who = (r.get('x_post') or {}).get('author')
    L.append(f"- [{r['source_url']}]({r['source_url']})" + (f" — @{who}" if who else ''))
    L.append(f"- {h('版权归原作者；本页仅摘要并链接。数据以 CC BY 4.0 发布。','Credit to the original author; this page only summarizes and links. Data under CC BY 4.0.')}")
    return '\n'.join(L) + '\n'
def main():
    out = R/'recipes'; out.mkdir(exist_ok=True)
    for f in out.glob('*.md'): f.unlink()
    idx_en = ['# Recipe guides', '', '[English](README.md) | [简体中文](README.zh-CN.md)', '', 'Step-by-step pages for a first batch of well-sourced recipes. New here? Read [Getting started](../docs/getting-started.md).', '', '| Recipe | Hardware | Level |', '|---|---|---|']
    idx_zh = ['# 配方指南', '', '[English](README.md) | [简体中文](README.zh-CN.md)', '', '首批来源可靠配方的分步页面。第一次来？先看 [入门指南](../docs/getting-started.zh-CN.md)。', '', '| 配方 | 硬件 | 来源等级 |', '|---|---|---|']
    for i in GUIDES:
        r = D[i]
        (out/f'{i}.md').write_text(page(r, 'en')); (out/f'{i}.zh-CN.md').write_text(page(r, 'zh'))
        idx_en.append(f"| [{en(r['model'])} · {en(r.get('engine')) or '—'}]({i}.md) | {en(r['hardware']) or r['hardware']} | {LV[r['source_level']][0]} |")
        idx_zh.append(f"| [{r['model']} · {r.get('engine') or '—'}]({i}.zh-CN.md) | {r['hardware']} | {LV[r['source_level']][1]} |")
    (out/'README.md').write_text('\n'.join(idx_en)+'\n'); (out/'README.zh-CN.md').write_text('\n'.join(idx_zh)+'\n')
    json.dump(GUIDES, open(R/'data/guides.json','w'))
    print(len(GUIDES), 'guides written')
if __name__ == '__main__': main()
