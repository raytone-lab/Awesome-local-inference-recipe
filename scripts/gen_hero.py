#!/usr/bin/env python3
"""Render README charts (en / zh-CN / ja). Needs matplotlib + a CJK font (Noto Sans CJK) for zh/ja labels.
- docs/hero{suf}.png          top 15 measured text setups ranked by tok/s per $1,000 of hardware
- docs/budget-tiers{suf}.png  fastest text setup per README budget tier (measured vs claimed)
Data: text recipes with tok_s and hardware_cost_usd; deduped per hardware+model (measured preferred, then best tok/s).
Not part of the CI up-to-date check (PNG bytes vary across matplotlib/font versions). Run: python3 scripts/gen_hero.py"""
import json, re
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib import font_manager as fm
R = Path(__file__).resolve().parent.parent
BOUNDS = [(0,2500),(2500,7000),(7000,14000),(14000,30000)]  # keep in sync with gen_readme.py
SUF = {'en':'','zh-CN':'.zh-CN','ja':'.ja'}
CJK = {'zh-CN':'Noto Sans CJK SC','ja':'Noto Sans CJK JP'}
FAM = {'Mac':'#7c3aed','NVIDIA 消费级':'#16a34a','DGX Spark':'#0ea5e9','AMD':'#dc2626','二手数据中心卡':'#f59e0b','其他':'#64748b'}
TX = {
 'en':dict(fam={'Mac':'Mac','NVIDIA 消费级':'NVIDIA consumer','DGX Spark':'DGX Spark','AMD':'AMD','二手数据中心卡':'Used datacenter','其他':'Other'},
   h_title='How much speed does $1,000 buy?  Top 15 measured setups',h_x='tok/s per $1,000 of hardware (single stream, measured)',
   b_title='Fastest setup in each budget tier',b_x='Best single-stream tok/s',meas='measured',claim='claimed / relayed',
   tiers=['≤ $2.5k','$2.5k–7k','$7k–14k','$14k–30k']),
 'zh-CN':dict(fam={'Mac':'Mac','NVIDIA 消费级':'NVIDIA 消费级','DGX Spark':'DGX Spark','AMD':'AMD','二手数据中心卡':'二手数据中心卡','其他':'其他'},
   h_title='每 $1000 能买到多少 tok/s？实测前 15 名',h_x='每 $1000 硬件对应的 tok/s（单流，实测）',
   b_title='各预算档最快的配置',b_x='最佳单流 tok/s',meas='实测',claim='宣称 / 转述',
   tiers=['≤ $2.5k','$2.5k–7k','$7k–14k','$14k–30k']),
 'ja':dict(fam={'Mac':'Mac','NVIDIA 消费级':'NVIDIA コンシューマー','DGX Spark':'DGX Spark','AMD':'AMD','二手数据中心卡':'中古データセンター','其他':'その他'},
   h_title='$1,000 でどれだけ速くなる？実測トップ 15',h_x='ハードウェア $1,000 あたりの tok/s（1 ストリーム、実測）',
   b_title='予算帯ごとの最速構成',b_x='1 ストリーム最高 tok/s',meas='実測',claim='公称 / 引用',
   tiers=['≤ $2.5k','$2.5k–7k','$7k–14k','$14k–30k']),
}
def clean(s,n):
    s=re.sub(r'[（(][^）)]*[）)]','',s); s=re.sub(r'[\u3000-\u30ff\u4e00-\u9fff，、；：]+',' ',s); s=re.sub(r'\s+',' ',s).strip(' +/·')
    return s if len(s)<=n else s[:n-1]+'…'
def money(x): return f'${x/1000:.1f}k' if x>=1000 else f'${x:.0f}'
D=[r for r in json.load(open(R/'data/recipes.json')) if r['category']=='text' and r['tok_s'] and r['hardware_cost_usd']]
best={}
for r in D:
    k=(clean(r['hardware'],80).lower(),clean(r['model'],80).lower()); cur=best.get(k)
    rank=lambda x:(x['source_level']=='实测',x['tok_s'],x['id'])
    if cur is None or rank(r)>rank(cur): best[k]=r
U=sorted(best.values(),key=lambda r:r['id'])
for r in U: r['_v']=r['tok_s']/r['hardware_cost_usd']*1000; r['_m']=r['source_level']=='实测'

def style(ax):
    for s in ('top','right'): ax.spines[s].set_visible(False)
def hero(lang):
    t=TX[lang]; top=sorted([r for r in U if r['_m']],key=lambda r:(-r['_v'],r['id']))[:15][::-1]
    fig,ax=plt.subplots(figsize=(11,6.2),dpi=150)
    for i,r in enumerate(top):
        ax.barh(i,r['_v'],color=FAM[r['hardware_family']],alpha=.9)
        ax.text(r['_v']+.6,i,f"{r['tok_s']:g} tok/s @ {money(r['hardware_cost_usd'])}",va='center',fontsize=9,color='#334155')
    ax.set_yticks(range(len(top))); ax.set_yticklabels([f"{clean(r['hardware'],30)} · {clean(r['model'],24)}" for r in top],fontsize=9)
    ax.set_xlabel(t['h_x']); ax.set_xlim(0,max(r['_v'] for r in top)*1.35)
    ax.set_title(t['h_title'],loc='left',fontsize=13,color='#0f172a'); style(ax); ax.grid(axis='x',alpha=.2)
    fams=[k for k in FAM if any(r['hardware_family']==k for r in top)]
    ax.legend(handles=[Patch(color=FAM[k],label=t['fam'][k]) for k in fams],frameon=False,loc='lower right',fontsize=9)
    return fig
def tiers(lang):
    t=TX[lang]; fig,ax=plt.subplots(figsize=(11,5.4),dpi=150); y=0; ticks=[]; xmax=0; used=set()
    for name,(lo,hi) in zip(t['tiers'],BOUNDS):
        rs=[r for r in U if lo<r['hardware_cost_usd']<=hi]; rows=[]
        for m in (True,False):
            pool=[r for r in rs if r['_m']==m]
            if pool: rows.append(max(pool,key=lambda r:(r['tok_s'],r['id'])))
        ys=[]
        for r in rows:
            c=FAM[r['hardware_family']]; used.add(r['hardware_family']); xmax=max(xmax,r['tok_s'])
            ax.barh(y,r['tok_s'],height=.8,color=c if r['_m'] else 'white',edgecolor=c,hatch=None if r['_m'] else '///',lw=1.2)
            ax.text(r['tok_s']+5,y,f"{r['tok_s']:g} tok/s · {clean(r['hardware'],28)} · {clean(r['model'],22)} · {money(r['hardware_cost_usd'])}",va='center',fontsize=8.5,color='#0f172a')
            ys.append(y); y-=1
        if ys: ticks.append(((ys[0]+ys[-1])/2,name))
        y-=.6
    ax.set_yticks([a for a,_ in ticks]); ax.set_yticklabels([b for _,b in ticks],fontsize=11,fontweight='bold')
    ax.set_xlim(0,xmax*1.9); ax.set_xlabel(t['b_x']); ax.set_title(t['b_title'],loc='left',fontsize=13,color='#0f172a')
    style(ax); ax.grid(axis='x',alpha=.2)
    h=[Patch(color=FAM[k],label=t['fam'][k]) for k in FAM if k in used]+[Patch(facecolor='white',edgecolor='#334155',hatch='///',label=t['claim'])]
    ax.legend(handles=h,frameon=False,loc='lower right',fontsize=9)
    return fig
if __name__=='__main__':
    have={f.name for f in fm.fontManager.ttflist}
    for lang,suf in SUF.items():
        plt.rcParams['font.family']=['DejaVu Sans']+([CJK[lang]] if lang in CJK and CJK[lang] in have else [])
        if lang in CJK and CJK[lang] not in have: print(f'warning: {CJK[lang]} not installed; CJK labels may render as boxes')
        for name,fn in (('hero',hero),('budget-tiers',tiers)):
            p=R/f'docs/{name}{suf}.png'; f=fn(lang); f.tight_layout(); f.savefig(p,facecolor='white',metadata={'Software':None}); plt.close(f); print(p.relative_to(R))
