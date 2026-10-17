#!/usr/bin/env python3
"""Static, crawlable parts of the Pages site (no JS needed to read them). Source of truth: data/recipes.json + recipes/*.md.
- explore.html: full static fallback table
- guides/<id>.html (+ zh-CN/ ja/): recipe guides from recipes/*.md; matching index.html per language; self-canonical + hreflang
- hw/<slug>.html, model/<slug>.html: landing pages
- sitemap.xml
Run: python3 scripts/gen_site.py"""
import json, re, html
from urllib.parse import quote
from pathlib import Path
import gen_readme
from dataset_constants import DATA_ASOF
from hardware_index import HW, MIN_ROWS, selfrep, single, meas_text, COMPARE
R = Path(__file__).resolve().parent.parent
PAGES = 'https://raytone-lab.github.io/awesome-local-inference-recipes/'
REPO = 'https://github.com/raytone-lab/awesome-local-inference-recipes'
STATIC_ROWS_START = '<!--static:rows (scripts/gen_site.py)-->'
STATIC_ROWS_END = '<!--/static-->'
D = json.load(open(R/'data/recipes.json', encoding='utf-8'))
ASOF = DATA_ASOF
LV = {'官方':'Official','实测':'Measured','转述':'Relayed','宣称':'Claimed'}
HWF = {'NVIDIA 消费级':'NVIDIA consumer','二手数据中心卡':'Used datacenter','其他':'Other'}
e = lambda s: html.escape(str(s if s is not None else ''), quote=True)
def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding='utf-8')
def normalize_punct(s): return s.replace('；', '; ').replace('，', ', ')
def en(s):
    if not s: return s
    return gen_readme.en(normalize_punct(str(s)), cjk=gen_readme.CJK_CHAR, strip=' ·+/,;；') or s
def met_en(r): return r.get('metric_en') or en(r.get('metric'))
def fen(r, k): return (r.get('en') or {}).get(k) or en(r.get(k))
def safe_url(u): return u if re.match(r'(https?:)?//|[\w./#?=&%-]+$', u) and not u.lower().startswith('javascript:') else '#'

def row(r):
    tok = '' if r.get('tok_s') is None else f"{r['tok_s']:g}"
    cost = f"{r['hardware_cost_usd']:,}" if r.get('hardware_cost_usd') is not None else e(fen(r, 'hardware_cost_text') or '')
    cpt = round(r['hardware_cost_usd']/r['tok_s']) if r.get('tok_s') and r.get('hardware_cost_usd') else ''
    met = met_en(r) or ''
    return (f'<tr data-id="{e(r["id"])}"><td></td><td>{e(fen(r, "model"))}</td><td>{e(fen(r, "quant") or "")}</td><td>{e(r["engine"])}</td>'
            f'<td>{e(fen(r, "hardware"))}</td><td class="n">{tok}</td><td>{e(met)}</td><td class="n">{cost}</td><td class="n">{cpt}</td>'
            f'<td>{e(fen(r, "context") or "")}</td><td><a href="{e(r["source_url"])}" rel="nofollow noopener">{LV.get(r["source_level"], e(r["source_level"]))}{" (self-reported)" if selfrep(r) else ""}</a> {e(r.get("date") or "")}</td></tr>')
def explore(links):
    p = R/'explore.html'; s = p.read_text(encoding='utf-8')
    rows = '\n'.join(row(r) for r in sorted(D, key=lambda r: (-(r.get('tok_s') or 0), r['id'])))
    s = re.sub(r'<tbody id="tb">.*?</tbody>', lambda m: f'<tbody id="tb">{STATIC_ROWS_START}\n{rows}\n{STATIC_ROWS_END}</tbody>', s, flags=re.S)
    nav = '<nav class="static-links" aria-label="Browse" data-i18n-al="nav_browse"><a href="guides/index.html" data-i18n="nav_guides">Guides &amp; hardware / model pages</a></nav>'
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
CHROME = {'en': ('Explore', 'Guides', 'Data as of', 'Local Inference Recipes', 'data CC BY 4.0'), 'zh-CN': ('配方库', '指南', '数据截至', '本地推理配方', '数据 CC BY 4.0'), 'ja': ('エクスプローラー', 'ガイド', 'データ時点', 'ローカル推論レシピ', 'データ CC BY 4.0')}
LANGS = [('en', '', '.md', 'en'), ('zh-CN', 'zh-CN/', '.zh-CN.md', 'zh-CN'), ('ja', 'ja/', '.ja.md', 'ja')]
PRE = {hl: pre for _, pre, _, hl in LANGS}
ORDER = [hl for *_, hl in LANGS]
SUF2PRE = {'': '', '.zh-CN': 'zh-CN/', '.ja': 'ja/'}
def shell(title, desc, canon, body, depth, lang='en', alts=None, noindex=False):
    up = '../'*depth
    gidx = 'guides/' + PRE[lang] + 'index.html'
    alt = ''.join(f'<link rel="alternate" hreflang="{hl}" href="{u}">' for hl, u in (alts or []))
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">{alt}{'<meta name="robots" content="noindex,follow">' if noindex else ''}
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{PAGES}docs/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{up}style.css"><script src="{up}theme.js"></script></head><body>
<header class="site-hd"><div class="hd-in"><a class="brand" href="{up}index.html">⚡ {CHROME[lang][3]}</a><nav class="static-links"><a href="{up}explore.html">{CHROME[lang][0]}</a> · <a href="{up}{gidx}">{CHROME[lang][1]}</a> · <a href="{REPO}">GitHub</a></nav></div></header>
<main class="doc static-page">
{body}
</main><footer class="site-ft"><div class="ft-in">{CHROME[lang][2]} {ASOF} · <a href="{REPO}">GitHub</a> · {CHROME[lang][4]}</div></footer></body></html>
'''

def guides():
    ids = sorted({p.name.split('.')[0] for p in (R/'recipes').glob('*.md') if not p.name.startswith('README')})
    available = {rid: {hl for _, pre, suf, hl in LANGS if (R/'recipes'/f'{rid}{suf}').exists()} for rid in ids}
    urls = []
    for rid in ids:
        alts = [(hl, f'{PAGES}guides/{PRE[hl]}{rid}.html') for hl in ORDER if hl in available[rid]]
        alts.append(('x-default', f'{PAGES}guides/{rid}.html'))
        for lang, pre, suf, hl in LANGS:
            src = R/'recipes'/f'{rid}{suf}'
            if not src.exists(): continue
            depth = 1 + (1 if pre else 0)
            def lm(u, depth=depth):
                m = re.match(r'^([\w.-]+?)(\.zh-CN|\.ja)?\.md$', u)
                if m and not u.startswith('../'):
                    return '../'*depth + 'guides/' + SUF2PRE[m.group(2) or ''] + m.group(1) + '.html'
                if u.startswith('../README'):
                    sm = re.match(r'^\.\./README(\.zh-CN|\.ja)?\.md$', u)
                    return '../'*depth + 'guides/' + SUF2PRE[(sm.group(1) if sm else '') or ''] + 'index.html'
                if u.startswith('../'): return f'{REPO}/blob/main/' + u[3:]
                return u
            text = src.read_text(encoding='utf-8')
            title = re.match(r'# (.*)', text).group(1)
            r = next((x for x in D if x['id'] == rid), {})
            desc = {'en': 'How to run {t}. Hardware, engine, launch command, and sourced speed ({lv}).',
                    'zh-CN': '{t} 运行指南。硬件、引擎、启动命令与有出处的速度（{lv}）。',
                    'ja': '{t} の実行ガイド。ハードウェア、エンジン、起動コマンド、出典付きの速度（{lv}）。'}[lang].format(t=title, lv=LVL[lang].get(r.get('source_level'), ''))
            sf = {'en': 'Source file', 'zh-CN': '源文件', 'ja': 'ソースファイル'}[lang]
            body = md(text, lm) + f'\n<p class="na">{sf}: <a href="{REPO}/blob/main/recipes/{rid}{suf}">recipes/{rid}{suf}</a></p>'
            canon = f'{PAGES}guides/{pre}{rid}.html'
            write(R/'guides'/f'{pre}{rid}.html', shell(title, desc, canon, body, depth, hl, alts)); urls.append(canon)
    return ids, urls, available

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
                f'The fastest measured single-device, single-stream text result is <b>{b["tok_s"]:g} tok/s</b> with {e(fen(b, "model"))}{eng} ({e(fen(b, "hardware"))}; '
                f'Measured{", " + e(b["date"]) if b.get("date") else ""}; <a href="{e(b["source_url"])}" rel="nofollow noopener">source</a>).')
    else:
        summ = (f'As of {ASOF}, this dataset has <b>{nrec(len(rows))}</b> for {e(name)}, {nmeas} of them measured by the poster'
                + ('.' if nmeas else '; none is first-hand yet, so treat the numbers below as official, claimed or relayed.')
                + (' These are image / video / audio results, so speed is given in the metric column rather than as tok/s.' if all(r['category'] != 'text' for r in rows) else ''))
    if dates: summ += (f' {len(dates)} of the entries carry a date' + (f' ({dates[0]}).' if dates[0] == dates[-1] else f', from {dates[0]} to {dates[-1]}.'))
    t = ['<table><thead><tr><th>Model</th><th>Engine</th><th>Hardware</th><th>tok/s</th><th>Metric</th><th>Source level</th><th>Date</th><th>Source</th></tr></thead><tbody>']
    for r in rows:
        tok = '' if r.get('tok_s') is None else f"{r['tok_s']:g}"
        t.append(f'<tr><td>{e(fen(r, "model"))}</td><td>{e(r["engine"])}</td><td>{e(fen(r, "hardware"))}</td><td class="n">{tok}</td><td>{e(met_en(r) or "")}</td><td>{LV.get(r["source_level"], "")}{" (self-reported)" if selfrep(r) else ""}</td><td>{e(r.get("date") or "")}</td><td><a href="{e(r["source_url"])}" rel="nofollow noopener">link</a></td></tr>')
    t.append('</tbody></table>')
    note = '<p class="na">Numbers come from each source. This project did not measure them again. Models and settings differ between rows. Source levels: Official = project or vendor; Measured = the poster ran it; Relayed = second-hand; Claimed = prediction or no reproduction details.</p>'
    qs = e({'hw': f'explore.html?q={quote(qterm or name)}', 'model': f'explore.html?family={quote(key)}'}[kind])
    body = f'<h1>{e(q)}</h1>\n<p>{summ}</p>\n<p><a href="../{qs}">Filter these in the explorer →</a></p>\n' + ''.join(t) + note
    canon = f'{PAGES}{kind}/{slug(key) if kind=="model" else key}.html'
    noidx = len(rows) < MIN_ROWS
    write(R/kind/f'{slug(key) if kind=="model" else key}.html', shell(q, re.sub('<[^>]+>', '', summ)[:300], canon, body, 1, 'en', None, noidx))
    return canon, noidx, len(rows)

def main():
    for d in ('guides', 'hw', 'model'):
        for p in (R/d).rglob('*.html') if (R/d).exists() else []: p.unlink()
    ids, gurls, available = guides()
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
    LANG_LABEL = {'en': 'English', 'zh-CN': '中文', 'ja': '日本語'}
    SWITCH_LABEL = {'en': 'English', 'zh-CN': '简体中文', 'ja': '日本語'}
    def resolve_lang(rid, want):
        have = available.get(rid, set())
        if want in have: return want
        for hl in ORDER:
            if hl in have: return hl
        return None
    def index_rel_href(rid, cur, want):
        tgt = resolve_lang(rid, want)
        if tgt is None: return None
        prefix = '' if cur == 'en' else '../'
        if tgt == cur: return f'{rid}.html'
        return prefix + PRE[tgt] + f'{rid}.html'
    def index_switch(cur):
        parts = []
        for hl in ORDER:
            href = 'index.html' if hl == cur else (('' if cur == 'en' else '../') + PRE[hl] + 'index.html')
            parts.append(f'<b>{SWITCH_LABEL[hl]}</b>' if hl == cur else f'<a href="{href}">{SWITCH_LABEL[hl]}</a>')
        return '<p>' + ' | '.join(parts) + '</p>'
    def guide_alts(rid, cur):
        bits = []
        for hl in ORDER:
            if hl == cur or resolve_lang(rid, hl) != hl: continue
            href = index_rel_href(rid, cur, hl)
            bits.append(f'<a href="{href}">{LANG_LABEL[hl]}</a>')
        return ('(' + ' · '.join(bits) + ')') if bits else ''
    def guide_label(r, lang):
        if lang == 'zh-CN':
            return f'{e(r.get("model") or "")} · {e(r.get("hardware") or "")}'
        return f'{e(fen(r, "model"))} · {e(fen(r, "hardware"))}'
    IDX = {
        'en': dict(title='Recipe guides · Local Inference Recipes',
                   desc='Step-by-step recipe guides, plus hardware and model speed pages. Each number has a source.',
                   h1='Recipe guides, hardware pages, and model pages',
                   intro=f'Pages built from the dataset (as of {ASOF}). Each number links to its source.',
                   h_g='Recipe guides', h_hw='By hardware', h_m='By model family', n=lambda c: f'{c} recipes'),
        'zh-CN': dict(title='配方指南 · 本地推理配方',
                   desc='分步配方指南，以及按硬件、按模型的速度页面。每个数字都有出处。',
                   h1='配方指南、硬件页面与模型页面',
                   intro=f'由数据集生成的页面（截至 {ASOF}）。每个数字都链接到来源。',
                   h_g='配方指南', h_hw='按硬件', h_m='按模型系列', n=lambda c: f'{c} 条'),
        'ja': dict(title='レシピガイド · ローカル推論レシピ',
                   desc='手順付きレシピガイドと、ハードウェア別・モデル別の速度ページ。数値はすべて出典付きです。',
                   h1='レシピガイド、ハードウェアページ、モデルページ',
                   intro=f'データセットから生成したページ（{ASOF} 時点）。すべての数値に出典へのリンクがあります。',
                   h_g='レシピガイド', h_hw='ハードウェア別', h_m='モデル系列別', n=lambda c: f'{c} 件'),
    }
    idx_alts = [(hl, f'{PAGES}guides/{PRE[hl]}index.html') for hl in ORDER]
    idx_alts.append(('x-default', f'{PAGES}guides/index.html'))
    idx_urls = []
    for lang, meta in IDX.items():
        depth = 1 if lang == 'en' else 2
        up = '../' * depth
        g = []
        for rid in ids:
            if rid not in byid or not available.get(rid): continue
            href = index_rel_href(rid, lang, lang)
            if not href: continue
            g.append(f'<li><a href="{href}">{guide_label(byid[rid], lang)}</a> {guide_alts(rid, lang)}</li>')
        hwl = [f'<li><a href="{up}{k}/{key}.html">{e(n)}</a> — {meta["n"](c)}</li>'
               for k, key, n, _, noidx, c in pages if k == 'hw' and not noidx]
        ml = [f'<li><a href="{up}{k}/{slug(key)}.html">{e(n)}</a> — {meta["n"](c)}</li>'
              for k, key, n, _, noidx, c in pages if k == 'model' and not noidx]
        body = (index_switch(lang) + f'<h1>{meta["h1"]}</h1><p>{meta["intro"]}</p>'
                f'<h2>{meta["h_g"]}</h2>{li(g)}<h2 id="by-hardware">{meta["h_hw"]}</h2>{li(hwl)}<h2>{meta["h_m"]}</h2>{li(ml)}')
        canon = f'{PAGES}guides/{PRE[lang]}index.html'
        write(R/'guides'/f'{PRE[lang]}index.html', shell(meta['title'], meta['desc'], canon, body, depth, lang, idx_alts))
        idx_urls.append(canon)
    explore(None)
    urls = [PAGES, PAGES+'explore.html', PAGES+'speed.html', PAGES+'submit.html'] + idx_urls + gurls + [c for *_, c, noidx, n in pages if not noidx]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f'<url><loc>{e(u)}</loc><lastmod>{ASOF}</lastmod></url>' for u in urls]
    sm.append('</urlset>')
    write(R/'sitemap.xml', '\n'.join(sm) + '\n')
    print(f'{len(gurls)} guide pages, {sum(1 for p in pages if not p[4])} indexable landing pages ({sum(1 for p in pages if p[4])} noindex), {len(urls)} sitemap URLs')
if __name__ == '__main__': main()
