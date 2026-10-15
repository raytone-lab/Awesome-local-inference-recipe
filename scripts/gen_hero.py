#!/usr/bin/env python3
"""Render README charts (en / zh-CN / ja). Needs matplotlib + a CJK font (Noto Sans CJK) for zh/ja labels.
- docs/hero{suf}.png          top measured text setups per model-size group (data/model-params.json), ranked by tok/s per $1,000 of hardware
- docs/budget-tiers{suf}.png  fastest text setup per README budget tier (measured vs claimed)
Data: text recipes with tok_s and hardware_cost_usd; deduped per hardware+model (measured preferred, then best tok/s).
Not part of the CI up-to-date check (PNG bytes vary across matplotlib/font versions). Run: python3 scripts/gen_hero.py"""
import re
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib import font_manager as fm
from hero_data import R, BOUNDS, clean, money, params, fmtb, load_setups, measured_with_card, title_row, grouped_rows, rtx3090_baseline, tier_rows, is_used, data_asof
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
U=load_setups()
def style(ax):
    for s in ('top','right'): ax.spines[s].set_visible(False)
HT={'en':dict(t='A {p} {u}{hw} runs {tok:g} tok/s',used='used ',
      sub='tok/s per $1,000 of hardware = single-stream tok/s ÷ (price / 1000) · measured results only · lowest published price, Oct 2026 · models differ per row',
      base='single RTX 3090 ≈{v:.0f}',note='Data as of {d} · CC BY 4.0 · Awesome Local Inference Recipes'),
    'zh-CN':dict(t='{p} 的{u}{hw} 就能跑 {tok:g} tok/s',used='二手 ',
      sub='每 $1000 的 tok/s = 单流 tok/s ÷（价格 / 1000）· 仅实测 · 价格取 2026 年 10 月公开最低价 · 各行模型不同',
      base='单张 RTX 3090 ≈{v:.0f}',note='数据截至 {d} · CC BY 4.0 · Awesome Local Inference Recipes'),
    'ja':dict(t='{p} の {u}{hw} で {tok:g} tok/s',used='中古 ',
      sub='$1,000 あたり tok/s = 1 ストリーム tok/s ÷（価格 / 1000）· 実測のみ · 2026 年 10 月の公開最安価格 · 行ごとにモデルは異なる',
      base='RTX 3090 1 枚 ≈{v:.0f}',note='データ時点 {d} · CC BY 4.0 · Awesome Local Inference Recipes')}
GT={'en':dict(dense='Dense ≥27B',big='Big MoE (≥100B total)',mid='Mid MoE (<100B total, ≥5B active)',small='Small MoE (<100B total, <5B active)',act='{a} active',tot='{a} active / {t} total',
              t='{p} {u}{hw} runs {m} at {tok:g} tok/s',flag=' ({f})',tern='ternary quant',mtp='MTP',sep=' + ',only='Discrete-GPU rows: card price only (Big MoE setups also need lots of system RAM) · Mac / DGX Spark: whole system · only models with official parameter cards (data/model-params.json)'),
    'zh-CN':dict(dense='稠密 ≥27B',big='大 MoE（总参数 ≥100B）',mid='中 MoE（总参数 <100B，激活 ≥5B）',small='小 MoE（总参数 <100B，激活 <5B）',act='激活 {a}',tot='激活 {a} / 总 {t}',
              t='{p} 的 {u}{hw} 跑 {m}：{tok:g} tok/s',flag='（{f}）',tern='三值量化',mtp='MTP',sep=' + ',only='独显行价格仅含显卡（大 MoE 配置还需大量系统内存）· Mac / DGX Spark 为整机价 · 仅含有官方参数卡的模型（data/model-params.json）'),
    'ja':dict(dense='Dense ≥27B',big='大型 MoE（総パラメータ ≥100B）',mid='中型 MoE（総 <100B、アクティブ ≥5B）',small='小型 MoE（総 <100B、アクティブ <5B）',act='アクティブ {a}',tot='アクティブ {a} / 総 {t}',
              t='{p} の {u}{hw} で {m} が {tok:g} tok/s',flag='（{f}）',tern='3 値量子化',mtp='MTP',sep=' + ',only='dGPU 行は GPU 本体価格のみ（大型 MoE 構成は大容量のメインメモリも必要）· Mac / DGX Spark は本体一式 · 公式パラメータカードのあるモデルのみ（data/model-params.json）')}
def hero(lang):
    t=TX[lang]; h=HT[lang]; g=GT[lang]
    meas=measured_with_card(U)
    rows,span=grouped_rows(meas)
    rows=[(k,g[x] if k=='h' else x) for k,x in rows]
    first=title_row(U)
    n=len(rows); H=1.2+.42*n; fig,ax=plt.subplots(figsize=(11.5,H),dpi=150)
    vmax=max(x['_v'] for k,x in rows if k=='r')
    for i,(k,x) in enumerate(rows):
        y=n-1-i
        if k=='h':
            ax.text(-.012,y,x,transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=10.5,fontweight='bold',color='#334155')
            if i: ax.axhline(y+.55,color='#e2e8f0',lw=.8)
            continue
        r=x; m=params(r)
        ax.barh(y,r['_v'],color=FAM[r['hardware_family']],alpha=.9,height=.72)
        ax.text(r['_v']+vmax*.01,y,f"≈{r['_v']:.0f} tok/s/$1k",va='center',fontsize=9.5,fontweight='bold',color='#0f172a')
        ax.annotate(f"({r['tok_s']:g} tok/s · {money(r['hardware_cost_usd'])})",(r['_v']+vmax*.01,y),xytext=(len(f"≈{r['_v']:.0f} tok/s/$1k")*6.4+4,0),textcoords='offset points',va='center',fontsize=8.5,color='#475569')
        ax.text(-.012,y+.13,f"{clean(r['hardware'],30)} [{money(r['hardware_cost_usd'])}]",transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=9.2,color='#0f172a')
        pa=g['act'].format(a=fmtb(m['active_b'])) if m['arch']=='dense' else g['tot'].format(a=fmtb(m['active_b']),t=m.get('total_label') or fmtb(m['total_b']))
        ax.text(-.012,y-.24,f"{clean(m['label'],26)} · {pa}",transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=7.3,color='#94a3b8')
    ax.set_yticks([]); ax.set_ylim(-.7,n-.3)
    bv=rtx3090_baseline(meas)
    if bv is not None and span:
        y0,y1=n-1-span[1]-.45,n-1-span[0]+.1
        ax.vlines(bv,y0,y1,linestyles=(0,(4,4)),lw=.8,color='#b6c0cf',alpha=.8,zorder=0)
        ax.text(bv,y1,' '+h['base'].format(v=bv),fontsize=8,color='#98a2b3',va='bottom')
    ax.set_xlim(0,vmax*1.6); ax.set_xlabel(t['h_x'],fontsize=10)
    hw=clean(first['hardware'],40); hw=re.sub(r'^(单 )','',hw)
    fl=[]
    if 'ternary' in first.get('tags',[]): fl.append(g['tern'])
    if 'MTP' in first.get('tags',[]): fl.append(g['mtp'])
    ftxt=g['flag'].format(f=g['sep'].join(fl)) if fl else ''
    fig.suptitle(g['t'].format(p=money(first['hardware_cost_usd']),u=h['used'] if is_used(first) else '',hw=re.sub(r' \d+GB$','',hw),m=params(first)['label'],tok=first['tok_s'])+ftxt,x=.012,y=.99,ha='left',fontsize=15,fontweight='bold',color='#0f172a')
    fig.text(.012,1-.62/H,h['sub'],ha='left',fontsize=9,color='#475569')
    fig.text(.012,1-.82/H,g['only'],ha='left',fontsize=8.5,color='#64748b')
    fig.text(.995,.006,h['note'].format(d=data_asof()),ha='right',fontsize=7.5,color='#94a3b8')
    style(ax); ax.spines['left'].set_visible(False); ax.grid(axis='x',alpha=.2)
    fams=[k for k in FAM if any(x['hardware_family']==k for kk,x in rows if kk=='r')]
    ax.legend(handles=[Patch(color=FAM[k],label=t['fam'][k]) for k in fams],frameon=False,loc='lower right',fontsize=8.5,ncol=1)
    fig.tight_layout(rect=(0,.015,1,1-.9/H)); fig.subplots_adjust(top=1-1.12/H)
    return fig
def tiers(lang):
    t=TX[lang]; fig,ax=plt.subplots(figsize=(11,5.4),dpi=150); y=0; ticks=[]; xmax=0; used=set()
    for name,(lo,hi) in zip(t['tiers'],BOUNDS):
        rows=tier_rows(U,lo,hi)
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
    fig.tight_layout()
    return fig
if __name__=='__main__':
    miss=sorted({r['model'] for r in U if r['_m'] and not params(r)})
    if miss: print('note: measured models without a data/model-params.json card (left off hero):',miss)
    have={f.name for f in fm.fontManager.ttflist}
    for lang,suf in SUF.items():
        plt.rcParams['font.family']=['DejaVu Sans']+([CJK[lang]] if lang in CJK and CJK[lang] in have else [])
        if lang in CJK and CJK[lang] not in have: print(f'warning: {CJK[lang]} not installed; CJK labels may render as boxes')
        for name,fn in (('hero',hero),('budget-tiers',tiers)):
            p=R/f'docs/{name}{suf}.png'; f=fn(lang); f.savefig(p,facecolor='white',metadata={'Software':None}); plt.close(f); print(p.relative_to(R))
