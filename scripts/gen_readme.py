#!/usr/bin/env python3
"""Generate README.md from data/recipes.json. Run: python3 scripts/gen_readme.py"""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = json.load(open(R/'data/recipes.json'))
LV = {'官方':'🏛️','实测':'✅','转述':'🔁','宣称':'📣'}
TIERS = [('tier-1-25k','Tier 1 · ≤ $2.5k',0,2500,'Used 3090/4090, MI50/V100 cards, Strix Halo, R9700'),
         ('tier-2-7k','Tier 2 · $2.5k–7k',2500,7000,'One RTX 5090, one DGX Spark, Mac Studio Max'),
         ('tier-3-14k','Tier 3 · $7k–14k',7000,14000,'Two Sparks, Mac Studio Ultra'),
         ('tier-4-30k','Tier 4 · $14k–30k',14000,30000,'3–4 Spark clusters, multi-GPU workstations')]
CATS = [('text','📝 Text'),('image','🖼️ Image'),('video-audio','🎬 Video & Audio')]
MAXTEXT = 10
def clip(s,n=90): s=(s or '').replace('|','/').replace('\n',' '); return s if len(s)<=n else s[:n-1]+'…'
def key(r):
    return f"**{r['tok_s']:g} tok/s**" if r['tok_s'] is not None else clip(r['metric'] or '未见公开数据',70)
def line(r):
    q = f" `{clip(r['quant'],28)}`" if r['quant'] else ''
    eng = '' if r['engine'].startswith('其他') else f" · {r['engine']}"
    return f"- **{r['model']}**{eng}{q} — {clip(r['hardware'],60)} → {key(r)} {LV.get(r['source_level'],'')} [source]({r['source_url']})"
def slug(s): return re.sub(r'[^a-z0-9 \-]','',s.lower()).replace(' ','-')
out=[]; toc=[]
def sec(level,title,anchor_title=None):
    out.append(f"\n{'#'*level} {title}\n")
    toc.append(('  '*(level-2))+f"- [{re.sub(r'^[^A-Za-z]+','',title)}](#{slug(anchor_title or title)})")
# --- body
seen=set();hot=[r for r in sorted([r for r in D if r.get('x_post')],key=lambda r:-(r['x_post']['likes']+3*r['x_post']['reposts'])) if not (r['source_url'] in seen or seen.add(r['source_url']))][:8]
sec(2,'Hot This Month')
out.append('Most-engaged recipe posts on X, 2026-09-15 → 10-13 (likes + 3×reposts).\n')
out += [f"- **{r['model']}** · {r['engine']} — {clip(r['hardware'],50)} → {key(r)} {LV[r['source_level']]} [@{r['x_post']['author']}]({r['source_url']}) ♥{r['x_post']['likes']}" for r in hot]
for a,t,lo,hi,desc in TIERS:
    sec(2,t)
    rs=[r for r in D if r['hardware_cost_usd'] is not None and lo<r['hardware_cost_usd']<=hi]
    out.append(f"*{desc}* · {len(rs)} recipes\n")
    for c,ct in CATS:
        cr=[r for r in rs if r['category']==c]
        if not cr: continue
        cr.sort(key=lambda r:-(r['tok_s'] or 0))
        out.append(f"\n**{ct}**\n")
        shown=cr[:MAXTEXT] if c=='text' else cr
        out += [line(r) for r in shown]
        if len(cr)>len(shown): out.append(f"- *…and {len(cr)-len(shown)} more in the [explorer](explore.html).*")
unk=[r for r in D if r['hardware_cost_usd'] is None]
sec(2,'Cost Not Published')
out.append(f"*Multi-card builds priced per card, Macs without a listed price, and other rows with no single published price* · {len(unk)} recipes. Top text recipes by tok/s:\n")
out += [line(r) for r in sorted([r for r in unk if r['tok_s']],key=lambda r:-r['tok_s'])[:12]]
out.append(f"- *…browse all {len(unk)} in the [explorer](explore.html).*")
body='\n'.join(out)
n={c:sum(r['category']==c for r in D) for c,_ in CATS}
STATIC=open(R/'scripts/readme_static.md').read()
head, tail = STATIC.split('<!--RECIPES-->')
toc_top = ['- [Legend](#legend)','- [Hot This Month](#hot-this-month)']+[x for x in toc if 'Hot This' not in x]+['- [Engines & Tools](#engines--tools)','- [Related Lists & Benchmarks](#related-lists--benchmarks)','- [Contributing](#contributing)','- [License](#license)']
head = head.replace('{{TOC}}','\n'.join(toc_top)).replace('{{N}}',str(len(D))).replace('{{NT}}',str(n['text'])).replace('{{NI}}',str(n['image'])).replace('{{NV}}',str(n['video-audio']))
open(R/'README.md','w').write(head+body+'\n'+tail)
print('README.md written,',len(D),'recipes')
