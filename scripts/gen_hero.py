#!/usr/bin/env python3
"""Render docs/hero.png: text-recipe tok/s vs hardware cost, colored by hardware family. Needs matplotlib.
Run: python3 scripts/gen_hero.py"""
import json
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
R = Path(__file__).resolve().parent.parent
D = [r for r in json.load(open(R/'data/recipes.json')) if r['category']=='text' and r['tok_s'] and r['hardware_cost_usd']]
FAM = {'Mac':('Mac','#7c3aed'),'NVIDIA 消费级':('NVIDIA consumer','#16a34a'),'DGX Spark':('DGX Spark','#0ea5e9'),
       'AMD':('AMD','#dc2626'),'二手数据中心卡':('Used datacenter','#f59e0b'),'其他':('Other','#64748b')}
fig, ax = plt.subplots(figsize=(12, 5), dpi=150)
for k,(lab,c) in FAM.items():
    rs=[r for r in D if r['hardware_family']==k]
    if not rs: continue
    m=[r for r in rs if r['source_level']=='实测']; o=[r for r in rs if r['source_level']!='实测']
    ax.scatter([r['hardware_cost_usd'] for r in m],[r['tok_s'] for r in m],s=46,c=c,alpha=.85,edgecolors='white',linewidths=.6,label=f'{lab} ({len(rs)})')
    ax.scatter([r['hardware_cost_usd'] for r in o],[r['tok_s'] for r in o],s=46,facecolors='none',edgecolors=c,alpha=.8,linewidths=1.1)
ax.set_xscale('log'); ax.set_xticks([500,1000,2500,5000,10000,30000]); ax.set_xticklabels(['$500','$1k','$2.5k','$5k','$10k','$30k'])
ax.set_xlim(300,32000); ax.set_ylim(0,None)
ax.set_xlabel('Lowest published hardware price (USD, log scale)',fontsize=11); ax.set_ylabel('Single-stream generation (tok/s)',fontsize=11)
ax.set_title(f'{len(D)} text recipes · tok/s vs hardware cost · filled = measured, hollow = official/relayed/claimed',fontsize=12,loc='left',color='#0f172a')
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(alpha=.25); ax.legend(frameon=False,fontsize=10,loc='upper left',ncol=3)
fig.tight_layout(); fig.savefig(R/'docs/hero.png',facecolor='white'); print('docs/hero.png')
