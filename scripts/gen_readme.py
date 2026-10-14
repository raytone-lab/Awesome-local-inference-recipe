#!/usr/bin/env python3
"""Generate README.md (English), README.zh-CN.md (Chinese) and README.ja.md (Japanese) from data/. Run: python3 scripts/gen_readme.py"""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = json.load(open(R/'data/recipes.json'))
REPOS = json.load(open(R/'data/repos.json'))
try: UPD = json.load(open(R/'data/repos.meta.json'))['updated_at']
except Exception: UPD = None
HWF_EN = {'NVIDIA 消费级':'NVIDIA consumer','二手数据中心卡':'Used datacenter GPU','其他':'Other'}
HWF_JA = {'NVIDIA 消费级':'NVIDIA コンシューマー','二手数据中心卡':'中古データセンター GPU','其他':'その他'}
PAGES = 'https://raytone-lab.github.io/Awesome-local-inference-recipe/'
GUIDES = set(json.load(open(R/'data/guides.json'))) if (R/'data/guides.json').exists() else set()
LVI = {'官方':'🏛️','实测':'✅','转述':'🔁','宣称':'📣'}
CJK = re.compile(r'[\u3000-\u303f\u3400-\u9fff\uff00-\uffef“”]')
L = {
 'en': dict(file='README.md', tpl='readme_static.en.md',
   tiers=['Tier 1 · up to $2.5k','Tier 2 · $2.5k–7k','Tier 3 · $7k–14k','Tier 4 · $14k–30k'],
   tdesc=['Used 3090/4090, MI50/V100 cards, Strix Halo, R9700','One RTX 5090, one DGX Spark, Mac Studio Max','Two Sparks, Mac Studio Ultra','3–4 Spark clusters, multi-GPU workstations'],
   cats={'text':'📝 Text','image':'🖼️ Image','video-audio':'🎬 Video & Audio'},
   fam='Browse by Model Family', famdesc='Click a family to open the explorer pre-filtered. Tags: {tags}.', engidx='Browse by Engine', engdesc='Engine names are normalized (`scripts/normalize_engines.py`); original strings are kept in `engine_note`.', th2='| Family | Recipes | Text | Image | Video & Audio |', th3='| Engine | Recipes |',
   hot='Hot This Month', hotdesc='Most-engaged recipe posts on X, 2026-09-15 → 10-13 (likes + 3×reposts).',
   unk='Cost Not Published', unkdesc='Multi-card builds priced per card, Macs without a listed price, and other rows without a single published price · {n} recipes. Top text recipes by tok/s:',
   guide='guide', gsuf='.md', more='…and {n} more in the [explorer](explore.html).', all='…browse all {n} in the [explorer](explore.html).', count='{n} recipes',
   src='source', see='see source', legend='Legend', eng='Engines & Tools', rel='Related Lists & Benchmarks', contrib='Contributing', lic='License',
   th='| Project | ⭐ Stars | Live | Last push | What |', site='*(site/blog)*', desc='desc',
   note='⭐ Snapshot updated {u} (UTC) by `scripts/update_stars.py` · *Live* badges are rendered by shields.io at view time.'),
 'zh': dict(file='README.zh-CN.md', tpl='readme_static.zh-CN.md',
   tiers=['第 1 档 · 2,500 美元以内','第 2 档 · 2,500–7,000 美元','第 3 档 · 7,000–14,000 美元','第 4 档 · 14,000–30,000 美元'],
   tdesc=['二手 3090/4090、MI50/V100、Strix Halo、R9700','单张 RTX 5090、单台 DGX Spark、Mac Studio Max','双 Spark、Mac Studio Ultra','3–4 台 Spark 集群、多卡工作站'],
   cats={'text':'📝 文字','image':'🖼️ 图像','video-audio':'🎬 影音'},
   fam='按模型系列浏览', famdesc='点击系列名即可打开已筛选的配方库。标签：{tags}。', engidx='按引擎浏览', engdesc='引擎名已统一（`scripts/normalize_engines.py`），原始写法保留在 `engine_note` 字段。', th2='| 系列 | 配方数 | 文字 | 图像 | 影音 |', th3='| 引擎 | 配方数 |',
   hot='本月热门', hotdesc='X 上互动最多的配方帖，2026-09-15 至 10-13（按 点赞 + 3×转发 排序）。',
   unk='价格未公开', unkdesc='按张计价的多卡组合、未标价格的 Mac 以及其他没有单一公开价格的配方 · 共 {n} 条。按 tok/s 排名靠前的文字配方：',
   guide='指南', gsuf='.zh-CN.md', more='……另有 {n} 条，见 [配方库](explore.html)。', all='……全部 {n} 条见 [配方库](explore.html)。', count='共 {n} 条',
   src='来源', see='见来源', legend='图例', eng='引擎与工具', rel='相关榜单与清单', contrib='参与贡献', lic='许可证',
   th='| 项目 | ⭐ Star | 实时 | 最后推送 | 简介 |', site='*（网站/博客）*', desc='desc_zh',
   note='⭐ 快照由 `scripts/update_stars.py` 更新于 {u}（UTC）· 「实时」徽章由 shields.io 在打开页面时实时渲染。'),
 'ja': dict(file='README.ja.md', tpl='readme_static.ja.md',
   tiers=['第 1 段階 · 2,500 ドルまで','第 2 段階 · 2,500〜7,000 ドル','第 3 段階 · 7,000〜14,000 ドル','第 4 段階 · 14,000〜30,000 ドル'],
   tdesc=['中古の 3090/4090、MI50/V100、Strix Halo、R9700','RTX 5090 1 枚、DGX Spark 1 台、Mac Studio Max','DGX Spark 2 台、Mac Studio Ultra','Spark 3〜4 台のクラスター、マルチ GPU ワークステーション'],
   cats={'text':'📝 テキスト','image':'🖼️ 画像','video-audio':'🎬 動画・音声'},
   fam='モデルファミリー別', famdesc='ファミリー名をクリックすると、絞り込み済みのエクスプローラーが開きます。タグ：{tags}。', engidx='エンジン別', engdesc='エンジン名は表記を統一しています（`scripts/normalize_engines.py`）。元の表記は `engine_note` に残しています。', th2='| ファミリー | レシピ数 | テキスト | 画像 | 動画・音声 |', th3='| エンジン | レシピ数 |',
   hot='今月の注目', hotdesc='2026-09-15〜10-13 に X で反応が多かったレシピ投稿（いいね + リポスト×3 の順）。',
   unk='価格非公開', unkdesc='1 枚単位で価格が出ているマルチ GPU 構成、価格の記載がない Mac など、単一の公開価格がないレシピ · {n} 件。tok/s 上位のテキストレシピ：',
   guide='手順', gsuf='.ja.md', more='…ほか {n} 件は[エクスプローラー](explore.html)で。', all='…全 {n} 件は[エクスプローラー](explore.html)で見られます。', count='{n} 件',
   src='出典', see='出典を参照', legend='凡例', eng='エンジンとツール', rel='関連リスト・ベンチマーク', contrib='コントリビュート', lic='ライセンス',
   th='| プロジェクト | ⭐ Star | ライブ | 最終 push | 概要 |', site='*（サイト・ブログ）*', desc='desc_ja',
   note='⭐ スナップショットは `scripts/update_stars.py` で {u}（UTC）に更新 · 「ライブ」バッジは表示時に shields.io が描画します。'),
}
BOUNDS=[(0,2500),(2500,7000),(7000,14000),(14000,30000)]
def clip(s,n=90): s=(s or '').replace('|','/').replace('\n',' '); return s if len(s)<=n else s[:n-1]+'…'
def en(s):
    """Drop Chinese fragments so English lines stay single-language (proper nouns kept)."""
    if not s: return s
    s=re.sub(r'（[^）]*）|\([^)]*[\u3400-\u9fff][^)]*\)','',s)
    s=' '.join(w for w in re.split(r'\s+',s) if not CJK.search(w))
    return re.sub(r'\s+',' ',s).strip(' ·+/,') or None
def slug(s): return re.sub(r'[^\w \-]','',s.lower()).replace(' ','-')
def fmt(n): return f"{n/1000:.1f}k" if n>=1000 else str(n)
import unicodedata
def _w(s): return len(s.encode('utf-16-le'))//2  # JS string length, as remark-lint measures
def _pad(s,w): return s+' '*(w-_w(s))
def _cells(l):
    l=l.strip()[1:-1]; out=[];cur='';i=0
    while i<len(l):
        c=l[i]
        if c=='\\' and i+1<len(l): cur+=l[i:i+2]; i+=2; continue
        if c=='|': out.append(cur.strip()); cur=''
        else: cur+=c
        i+=1
    out.append(cur.strip()); return out
def align_tables(txt):
    """Pad markdown tables so pipes align (remark-lint table-pipe-alignment / cell-padding)."""
    lines=txt.split('\n'); res=[]; i=0
    while i<len(lines):
        if lines[i].startswith('|') and i+1<len(lines) and re.match(r'^\|[\s:|-]+\|$',lines[i+1].strip()):
            j=i
            while j<len(lines) and lines[j].startswith('|'): j+=1
            rows=[_cells(l) for l in lines[i:j]]; n=max(map(len,rows))
            rows=[r+['']*(n-len(r)) for r in rows]
            w=[max(3,max(_w(r[k]) for k_,r in enumerate(rows) if k_!=1)) for k in range(n)]
            for k_,r in enumerate(rows):
                if k_==1: res.append('| '+' | '.join('-'*w[k] for k in range(n))+' |')
                else: res.append('| '+' | '.join(_pad(r[k],w[k]) for k in range(n))+' |')
            i=j
        else: res.append(lines[i]); i+=1
    return '\n'.join(res)
def build(lang):
    T=L[lang]; E=(lambda s:en(s)) if lang in ('en','ja') else (lambda s:s)
    def key(r):
        if r['tok_s'] is not None: return f"**{r['tok_s']:g} tok/s**"
        m=(r.get('metric_en') or r['metric']) if lang in ('en','ja') else r['metric']
        if lang in ('en','ja') and m and CJK.search(m): m=None  # don't show mangled partial translations
        return clip(m,70) if m else T['see']
    def ln(r):
        q=E(r['quant']); q=f" `{clip(q,28)}`" if q else ''
        eg=E(r['engine']); eg='' if (not eg or r['engine']=='Unspecified') else f" · {eg}"
        return f"- **{E(r['model'])}**{eg}{q} — {clip(E(r['hardware']) or ({'en':HWF_EN,'ja':HWF_JA}.get(lang,{}).get(r['hardware_family'],r['hardware_family'])),60)} → {key(r)} {LVI.get(r['source_level'],'')} [{T['src']}]({r['source_url']})"+(f" · [{T['guide']}](recipes/{r['id']}{T['gsuf']})" if r['id'] in GUIDES else '')
    out=[];toc=[]
    def sec(t): out.append(f"\n## {t}\n"); toc.append(f"- [{t}](#{slug(t)})")
    seen=set();hot=[r for r in sorted([r for r in D if r.get('x_post')],key=lambda r:-(r['x_post']['likes']+3*r['x_post']['reposts'])) if not (r['source_url'] in seen or seen.add(r['source_url']))][:8]
    sec(T['hot']); out.append(T['hotdesc']+'\n')
    for r in hot:
        eg=E(r['engine']); eg=f" · {eg}" if eg and r['engine']!='Unspecified' else ''
        out.append(f"- **{E(r['model'])}**{eg} — {clip(E(r['hardware']),50)} → {key(r)} {LVI[r['source_level']]} [@{r['x_post']['author']}]({r['source_url']}) ♥{r['x_post']['likes']}")
    from collections import Counter
    from urllib.parse import quote
    sec(T['fam']); fc=Counter(r['model_family'] for r in D); tc=Counter(t for r in D for t in r['tags'])
    tl=', '.join(f"[`{t}`](explore.html?tag={quote(t)}) {n}" for t,n in tc.most_common())
    out.append(T['famdesc'].format(tags=tl)+'\n'); out.append(T['th2']); out.append('|---|--:|--:|--:|--:|')
    for f,n in sorted(fc.items(),key=lambda x:(x[0]=='Other',-x[1],x[0])):
        cc=[sum(1 for r in D if r['model_family']==f and r['category']==c) or '' for c in ('text','image','video-audio')]
        out.append(f"| [{f}](explore.html?family={quote(f)}) | {n} | "+' | '.join(map(str,cc))+' |')
    sec(T['engidx']); out.append(T['engdesc']+'\n'); out.append(T['th3']); out.append('|---|--:|')
    for e,n in sorted(Counter(r['engine'] for r in D).items(),key=lambda x:(x[0]=='Unspecified',-x[1],x[0])):
        out.append(f"| [{e}](explore.html?engine={quote(e)}) | {n} |")
    for t,d,(lo,hi) in zip(T['tiers'],T['tdesc'],BOUNDS):
        sec(t); rs=[r for r in D if r['hardware_cost_usd'] is not None and lo<r['hardware_cost_usd']<=hi]
        out.append(f"*{d}* · {T['count'].format(n=len(rs))}\n")
        for c,ct in T['cats'].items():
            cr=sorted([r for r in rs if r['category']==c],key=lambda r:-(r['tok_s'] or 0))
            if not cr: continue
            out.append(f"\n**{ct}**\n"); sh=cr[:10] if c=='text' else cr
            out+= [ln(r) for r in sh]
            if len(cr)>len(sh): out.append('- *'+T['more'].format(n=len(cr)-len(sh))+'*')
    unk=[r for r in D if r['hardware_cost_usd'] is None]
    sec(T['unk']); out.append(T['unkdesc'].format(n=len(unk))+'\n')
    out+= [ln(r) for r in sorted([r for r in unk if r['tok_s']],key=lambda r:-r['tok_s'])[:12]]
    out.append('- *'+T['all'].format(n=len(unk))+'*')
    def rtable(s):
        rows=[T['th'],"|---|--:|---|---|---|"]
        for r in sorted([r for r in REPOS if r['section']==s],key=lambda r:-(r.get('stars') or -1)):
            url=r.get('url') or f"https://github.com/{r['repo']}"
            if r.get('repo'): st=fmt(r['stars']) if r.get('stars') is not None else '—'; lv=f"![stars](https://img.shields.io/github/stars/{r['repo']}?style=flat&label=)"; pu=(r.get('pushed_at') or '')[:10] or '—'
            else: st,lv,pu='—',T['site'],'—'
            rows.append(f"| [{r['name']}]({url}) | {st} | {lv} | {pu} | {r[T['desc']]} |")
        return '\n'.join(rows)+(f"\n\n<sub>{T['note'].format(u=UPD)}</sub>" if UPD else '')
    tpl=open(R/'scripts'/T['tpl']).read(); head,tail=tpl.split('<!--RECIPES-->')
    n={c:sum(r['category']==c for r in D) for c in T['cats']}
    toc=[f"- [{T['legend']}](#{slug(T['legend'])})"]+toc+[f"- [{x}](#{slug(x)})" for x in (T['eng'],T['rel'],T['lic'])]
    head=head.replace('{{TOC}}','\n'.join(toc)).replace('{{N}}',str(len(D))).replace('{{NT}}',str(n['text'])).replace('{{NI}}',str(n['image'])).replace('{{NV}}',str(n['video-audio']))
    tail=tail.replace('<!--ENGINES-->',rtable('engines')).replace('<!--RELATED-->',rtable('related'))
    txt=head+'\n'.join(out)+'\n'+tail
    for pg in ('explore.html','submit.html'):
        txt=txt.replace(f'](%s'%pg,f']({PAGES}{pg}').replace(f'href="{pg}','href="'+PAGES+pg)
    txt=align_tables(txt)
    open(R/T['file'],'w').write(txt)
    return T['file']
for lang in L: print('written', build(lang))
