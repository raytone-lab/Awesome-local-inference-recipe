#!/usr/bin/env python3
"""Static, crawlable parts of the Pages site (no JS needed to read them). Source of truth: data/recipes.json + recipes/*.md.
- explore.html: full static fallback table
- guides/<id>.html, guides/zh-CN/<id>.html, guides/ja/<id>.html: recipe guides rendered from recipes/*.md, self-canonical + hreflang
- hw/<slug>.html, model/<slug>.html: landing pages
- guides/index.html: crawlable index of guides and landing pages
- sitemap.xml
Run: python3 scripts/gen_site.py"""
import json, re, html
from urllib.parse import quote
from pathlib import Path
from typing import NamedTuple
import gen_readme
from dataset_constants import DATA_ASOF
R = Path(__file__).resolve().parent.parent
PAGES = 'https://raytone-lab.github.io/awesome-local-inference-recipes/'
REPO = 'https://github.com/raytone-lab/awesome-local-inference-recipes'
MIN_ROWS = 5
STATIC_ROWS_START = '<!--static:rows (scripts/gen_site.py)-->'
STATIC_ROWS_END = '<!--/static-->'
D = json.load(open(R/'data/recipes.json', encoding='utf-8'))
ASOF = DATA_ASOF
LV = {'官方':'Official','实测':'Measured','转述':'Relayed','宣称':'Claimed'}
HWF = {'NVIDIA 消费级':'NVIDIA consumer','二手数据中心卡':'Used datacenter','其他':'Other'}
e = lambda s: html.escape(str(s if s is not None else ''), quote=True)
def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding='utf-8')
def selfrep(r): return '自称' in (r.get('metric') or '')
def normalize_punct(s): return s.replace('；', '; ').replace('，', ', ')
def en(s):
    if not s: return s
    return gen_readme.en(normalize_punct(str(s)), cjk=gen_readme.CJK_CHAR, strip=' ·+/,;；') or s
def met_en(r): return r.get('metric_en') or en(r.get('metric'))
COMPARE = re.compile(r'\s/|/\s|\svs\.?\s', re.I)
def single(r):
    return ('multi-GPU' not in r['tags'] and not re.search(r'[2-9] ?[x×] ?|双|[2-9] ?台', r['hardware']) and not COMPARE.search(r['hardware'])
            and not r.get('superseded_by') and not re.search(r'并发|aggregate|总吞吐', (r.get('metric') or '') + ' ' + str(r.get('concurrency') or ''), re.I))
def meas_text(r): return r['source_level'] == '实测' and r['category'] == 'text' and r.get('tok_s') and not selfrep(r)
def safe_url(u): return u if re.match(r'(https?:)?//|[\w./#?=&%-]+$', u) and not u.lower().startswith('javascript:') else '#'

def row(r):
    tok = '' if r.get('tok_s') is None else f"{r['tok_s']:g}"
    cost = f"{r['hardware_cost_usd']:,}" if r.get('hardware_cost_usd') is not None else e(r.get('hardware_cost_text') or '')
    cpt = round(r['hardware_cost_usd']/r['tok_s']) if r.get('tok_s') and r.get('hardware_cost_usd') else ''
    met = met_en(r) or ''
    return (f'<tr data-id="{e(r["id"])}"><td></td><td>{e(en(r["model"]))}</td><td>{e(r.get("quant") or "")}</td><td>{e(r["engine"])}</td>'
            f'<td>{e(en(r["hardware"]))}</td><td class="n">{tok}</td><td>{e(met)}</td><td class="n">{cost}</td><td class="n">{cpt}</td>'
            f'<td>{e(r.get("context") or "")}</td><td><a href="{e(r["source_url"])}" rel="nofollow noopener">{LV.get(r["source_level"], e(r["source_level"]))}{" (self-reported)" if selfrep(r) else ""}</a> {e(r.get("date") or "")}</td></tr>')
def explore(links):
    p = R/'explore.html'; s = p.read_text(encoding='utf-8')
    rows = '\n'.join(row(r) for r in sorted(D, key=lambda r: (-(r.get('tok_s') or 0), r['id'])))
    s = re.sub(r'<tbody id="tb">.*?</tbody>', lambda m: f'<tbody id="tb">{STATIC_ROWS_START}\n{rows}\n{STATIC_ROWS_END}</tbody>', s, flags=re.S)
    nav = '<nav class="static-links" aria-label="Browse"><a href="guides/index.html">Guides &amp; hardware / model pages</a></nav>'
    blk = f'<!--static:links-->{nav}<!--/static:links-->'
    if '<!--static:links-->' in s: s = re.sub(r'<!--static:links-->.*?<!--/static:links-->', lambda m: blk, s, flags=re.S)
    else: s = s.replace('<div class="more" id="morew"', blk + '\n<div class="more" id="morew"', 1)
    write(p, s)

def inline(t, linkmap):
    out = []; i = 0
    for m in re.finditer(r'`([^`]+)`|\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)\s]+)\)', t):
        out.append(e(t[i:m.start()]))
        if m.group(1) is not None: out.append(f'<code>{e(m.group(1))}</code>')
        elif m.group(2) is not None: out.append(f'<b>{inline(m.group(2), linkmap)}</b>')
        else:
            u = safe_url(linkmap(m.group(4))); ext = u.startswith('http')
            out.append(f'<a href="{e(u)}"{" rel=\"nofollow noopener\"" if ext else ""}>{inline(m.group(3), linkmap)}</a>')
        i = m.end()
    out.append(e(t[i:])); return ''.join(out)
def md(src, linkmap):
    L = src.split('\n'); h = []; i = 0; lst = False
    def close():
        nonlocal lst
        if lst: h.append('</ul>'); lst = False
    while i < len(L):
        l = L[i]
        if l.startswith('```'):
            close(); j = i+1; buf = []
            while j < len(L) and not L[j].startswith('```'): buf.append(L[j]); j += 1
            h.append(f'<pre><code>{e(chr(10).join(buf))}</code></pre>'); i = j+1; continue
        m = re.match(r'(#{1,3}) (.*)', l)
        if m: close(); n = len(m.group(1)); h.append(f'<h{n}>{inline(m.group(2), linkmap)}</h{n}>')
        elif l.startswith('- '):
            if not lst: h.append('<ul>'); lst = True
            h.append(f'<li>{inline(l[2:], linkmap)}</li>')
        elif l.startswith('> '): close(); h.append(f'<blockquote>{inline(l[2:], linkmap)}</blockquote>')
        elif l.strip(): close(); h.append(f'<p>{inline(l, linkmap)}</p>')
        else: close()
        i += 1
    close(); return '\n'.join(h)

LVL = {'en': LV, 'zh-CN': {k: k for k in LV}, 'ja': {'官方': '公式', '实测': '実測', '转述': '伝聞', '宣称': '主張'}}
CHROME = {'en': ('Explore', 'Guides', 'Data as of'), 'zh-CN': ('配方库', '指南', '数据截至'), 'ja': ('エクスプローラー', 'ガイド', 'データ時点')}
LANGS = [('en', '', '.md', 'en'), ('zh-CN', 'zh-CN/', '.zh-CN.md', 'zh-CN'), ('ja', 'ja/', '.ja.md', 'ja')]
def shell(title, desc, canon, body, depth, lang='en', alts=None, noindex=False):
    up = '../'*depth
    alt = ''.join(f'<link rel="alternate" hreflang="{hl}" href="{u}">' for hl, u in (alts or []))
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">{alt}{'<meta name="robots" content="noindex,follow">' if noindex else ''}
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{PAGES}docs/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{up}style.css"><script src="{up}theme.js"></script></head><body>
<header class="site-hd"><div class="hd-in"><a class="brand" href="{up}index.html">⚡ Local Inference Recipes</a><nav class="static-links"><a href="{up}explore.html">{CHROME[lang][0]}</a> · <a href="{up}guides/index.html">{CHROME[lang][1]}</a> · <a href="{REPO}">GitHub</a></nav></div></header>
<main class="doc static-page">
{body}
</main><footer class="site-ft"><div class="ft-in">{CHROME[lang][2]} {ASOF} · <a href="{REPO}">GitHub</a> · data CC BY 4.0</div></footer></body></html>
'''

def guides():
    ids = sorted({p.name.split('.')[0] for p in (R/'recipes').glob('*.md') if not p.name.startswith('README')})
    urls = []
    for rid in ids:
        alts = [(hl, f'{PAGES}guides/{pre}{rid}.html') for _, pre, suf, hl in LANGS if (R/'recipes'/f'{rid}{suf}').exists()]
        alts.append(('x-default', f'{PAGES}guides/{rid}.html'))
        for lang, pre, suf, hl in LANGS:
            src = R/'recipes'/f'{rid}{suf}'
            if not src.exists(): continue
            depth = 1 + (1 if pre else 0)
            def lm(u, pre=pre, depth=depth):
                m = re.match(r'^([\w.-]+?)(\.zh-CN|\.ja)?\.md$', u)
                if m and not u.startswith('../'):
                    tgt = {'' : '', '.zh-CN': 'zh-CN/', '.ja': 'ja/'}[m.group(2) or '']
                    return '../'*depth + 'guides/' + tgt + m.group(1) + '.html'
                if u.startswith('../README'): return '../'*depth + 'guides/index.html'
                if u.startswith('../'): return f'{REPO}/blob/main/' + u[3:]
                return u
            text = src.read_text(encoding='utf-8')
            title = re.match(r'# (.*)', text).group(1)
            r = next((x for x in D if x['id'] == rid), {})
            desc = {'en': 'How to run {t}: hardware, engine, launch command and the sourced speed ({lv}).',
                    'zh-CN': '{t} 的运行指南：硬件、引擎、启动命令与有出处的速度（{lv}）。',
                    'ja': '{t} の実行ガイド：ハードウェア、エンジン、起動コマンド、出典付きの速度（{lv}）。'}[lang].format(t=title, lv=LVL[lang].get(r.get('source_level'), ''))
            sf = {'en': 'Source file', 'zh-CN': '源文件', 'ja': 'ソースファイル'}[lang]
            body = md(text, lm) + f'\n<p class="na">{sf}: <a href="{REPO}/blob/main/recipes/{rid}{suf}">recipes/{rid}{suf}</a></p>'
            canon = f'{PAGES}guides/{pre}{rid}.html'
            write(R/'guides'/f'{pre}{rid}.html', shell(title, desc, canon, body, depth, hl, alts)); urls.append(canon)
    return ids, urls

class HardwarePage(NamedTuple):
    slug: str
    name: str
    pattern: str
    explorer_query: str
HW = [
 HardwarePage('rtx-5090','RTX 5090',r'RTX 5090','RTX 5090'),HardwarePage('rtx-4090','RTX 4090',r'RTX 4090','RTX 4090'),HardwarePage('rtx-3090','RTX 3090',r'RTX 3090','RTX 3090'),HardwarePage('rtx-5060-ti','RTX 5060 Ti',r'RTX 5060 Ti','RTX 5060 Ti'),
 HardwarePage('mac-studio-m3-ultra','Mac Studio M3 Ultra',r'M3 Ultra','M3 Ultra'),HardwarePage('mac-m4-max','Apple M4 Max',r'M4 Max','M4 Max'),HardwarePage('mac-m5','Apple M5 Pro / M5 Max',r'M5 (Pro|Max)','M5'),
 HardwarePage('dgx-spark','NVIDIA DGX Spark',r'DGX Spark','DGX Spark'),HardwarePage('strix-halo','AMD Strix Halo (Ryzen AI Max+ 395)',r'Strix Halo','Strix Halo'),
 HardwarePage('amd-radeon','AMD Radeon (RX 7900 / R9700)',r'RX 7900|R9700','R9700'),HardwarePage('tesla-p40','NVIDIA Tesla P40',r'P40','P40'),HardwarePage('rtx-pro-6000','RTX PRO 6000',r'RTX PRO 6000','RTX PRO 6000')]
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def landing(kind, key, name, rows, qterm=None):
    rows = sorted(rows, key=lambda r: (r['source_level'] != '实测', -(r.get('tok_s') or 0), r['id']))
    meas = [r for r in rows if meas_text(r) and single(r)]
    nmeas = sum(1 for r in rows if r['source_level'] == '实测' and not selfrep(r))
    nrec = lambda n: f'{n} recipe' + ('' if n == 1 else 's')
    dates = sorted(r['date'] for r in rows if r.get('date'))
    q = f'{name}: local inference speed (tok/s), sourced' if kind=='model' else f'Setups with {name}: local inference speed (tok/s), sourced'
    if meas:
        b = max(meas, key=lambda r: (r['tok_s'], r['id']))
        eng = '' if b['engine'] == 'Unspecified' else f' on {e(b["engine"])}'
        summ = (f'As of {ASOF}, this dataset has <b>{nrec(len(rows))}</b> for {e(name)}, {nmeas} of them measured by the poster. '
                f'The fastest measured single-device, single-stream text result is <b>{b["tok_s"]:g} tok/s</b> with {e(en(b["model"]))}{eng} ({e(en(b["hardware"]))}; '
                f'Measured{", " + e(b["date"]) if b.get("date") else ""}; <a href="{e(b["source_url"])}" rel="nofollow noopener">source</a>).')
    else:
        summ = (f'As of {ASOF}, this dataset has <b>{nrec(len(rows))}</b> for {e(name)}, {nmeas} of them measured by the poster'
                + ('.' if nmeas else '; none is first-hand yet, so treat the numbers below as official, claimed or relayed.')
                + (' These are image / video / audio results, so speed is given in the metric column rather than as tok/s.' if all(r['category'] != 'text' for r in rows) else ''))
    if dates: summ += (f' {len(dates)} of the entries carry a date' + (f' ({dates[0]}).' if dates[0] == dates[-1] else f', from {dates[0]} to {dates[-1]}.'))
    t = ['<table><thead><tr><th>Model</th><th>Engine</th><th>Hardware</th><th>tok/s</th><th>Metric</th><th>Source level</th><th>Date</th><th>Source</th></tr></thead><tbody>']
    for r in rows:
        tok = '' if r.get('tok_s') is None else f"{r['tok_s']:g}"
        t.append(f'<tr><td>{e(en(r["model"]))}</td><td>{e(r["engine"])}</td><td>{e(en(r["hardware"]))}</td><td class="n">{tok}</td><td>{e(met_en(r) or "")}</td><td>{LV.get(r["source_level"], "")}{" (self-reported)" if selfrep(r) else ""}</td><td>{e(r.get("date") or "")}</td><td><a href="{e(r["source_url"])}" rel="nofollow noopener">link</a></td></tr>')
    t.append('</tbody></table>')
    note = '<p class="na">Numbers are quoted from each source and have not been re-run by this project. Models and settings differ between rows. Source levels: Official = project/vendor, Measured = the poster ran it, Relayed = second-hand, Claimed = prediction or no reproduction details.</p>'
    qs = e({'hw': f'explore.html?q={quote(qterm or name)}', 'model': f'explore.html?family={quote(key)}'}[kind])
    body = f'<h1>{e(q)}</h1>\n<p>{summ}</p>\n<p><a href="../{qs}">Filter these in the explorer →</a></p>\n' + ''.join(t) + note
    canon = f'{PAGES}{kind}/{slug(key) if kind=="model" else key}.html'
    noidx = len(rows) < MIN_ROWS
    write(R/kind/f'{slug(key) if kind=="model" else key}.html', shell(q, re.sub('<[^>]+>', '', summ)[:300], canon, body, 1, 'en', None, noidx))
    return canon, noidx, len(rows)

def main():
    for d in ('guides', 'hw', 'model'):
        for p in (R/d).rglob('*.html') if (R/d).exists() else []: p.unlink()
    ids, gurls = guides()
    pages = []
    for key, name, rx, qt in HW:
        rows = [r for r in D if re.search(rx, r['hardware'])]
        if rows: pages.append(('hw', key, name) + landing('hw', key, name, rows, qt))
    fams = sorted({r['model_family'] for r in D if r['model_family'] != 'Other'})
    for f in fams:
        rows = [r for r in D if r['model_family'] == f]
        pages.append(('model', f, f) + landing('model', f, f, rows))
    li = lambda items: '<ul>' + ''.join(items) + '</ul>'
    byid = {r['id']: r for r in D}
    g = [f'<li><a href="{rid}.html">{e(en(byid[rid]["model"]))} · {e(en(byid[rid]["hardware"]))}</a> (<a href="zh-CN/{rid}.html">中文</a> · <a href="ja/{rid}.html">日本語</a>)</li>' for rid in ids if rid in byid]
    hwl = [f'<li><a href="../{k}/{(slug(key) if k=="model" else key)}.html">{e(n)}</a> — {c} recipes</li>' for k, key, n, _, noidx, c in pages if k == 'hw' and not noidx]
    ml = [f'<li><a href="../{k}/{slug(key)}.html">{e(n)}</a> — {c} recipes</li>' for k, key, n, _, noidx, c in pages if k == 'model' and not noidx]
    body = (f'<h1>Local inference recipe guides, hardware and model pages</h1><p>Static pages generated from the dataset (as of {ASOF}). Every number links to its source.</p>'
            f'<h2>Recipe guides</h2>{li(g)}<h2>By hardware</h2>{li(hwl)}<h2>By model family</h2>{li(ml)}')
    write(R/'guides/index.html', shell('Recipe guides · Local Inference Recipes', 'Step-by-step local inference recipe guides plus per-hardware and per-model speed pages, every number sourced.', f'{PAGES}guides/index.html', body, 1))
    explore(None)
    urls = [PAGES, PAGES+'explore.html', PAGES+'speed.html', PAGES+'submit.html', PAGES+'guides/index.html'] + gurls + [c for *_, c, noidx, n in pages if not noidx]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f'<url><loc>{e(u)}</loc><lastmod>{ASOF}</lastmod></url>' for u in urls]
    sm.append('</urlset>')
    write(R/'sitemap.xml', '\n'.join(sm) + '\n')
    print(f'{len(gurls)} guide pages, {sum(1 for p in pages if not p[4])} indexable landing pages ({sum(1 for p in pages if p[4])} noindex), {len(urls)} sitemap URLs')
if __name__ == '__main__': main()
