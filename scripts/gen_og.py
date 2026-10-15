#!/usr/bin/env python3
"""Render docs/og.png (1280x640 social preview, English). No data numbers on purpose, so it never goes stale.
Upload it manually in GitHub repo Settings → Social preview; the Pages site references it via og:image. Run: python3 scripts/gen_og.py"""
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parent.parent
fig=plt.figure(figsize=(12.8,6.4),dpi=100); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1280); ax.set_ylim(0,640); ax.axis('off')
ax.add_patch(plt.Rectangle((0,0),1280,640,color='#0f172a'))
ax.add_patch(plt.Rectangle((0,0),1280,10,color='#4f46e5'))
ax.text(80,520,'⚡ Awesome Local Inference Recipes',fontsize=40,fontweight='bold',color='white',va='center')
ax.text(80,440,'Model × engine × hardware → real tok/s and cost.',fontsize=27,color='#cbd5e1',va='center')
ax.text(80,392,'Every number linked to its source and trust level.',fontsize=27,color='#cbd5e1',va='center')
x=80
for t,c in [('measured','#16a34a'),('official','#4f46e5'),('relayed','#d97706'),('claimed','#dc2626')]:
    w=len(t)*15+44; ax.add_patch(FancyBboxPatch((x,268),w,48,boxstyle='round,pad=0,rounding_size=24',color=c)); ax.text(x+w/2,292,t,fontsize=19,color='white',ha='center',va='center'); x+=w+18
ax.text(80,180,'Explore · filter · compare   |   Feel the speed: 10 → 500 tok/s',fontsize=21,color='#e2e8f0',va='center')
ax.text(80,130,'raytone-lab.github.io/Awesome-local-inference-recipe',fontsize=18,color='#818cf8',va='center')
ax.text(1200,40,'llama.cpp · MLX · vLLM · SGLang · Strata · oMLX · ≤ $30k',fontsize=16,color='#64748b',ha='right')
fig.savefig(R/'docs/og.png',facecolor='#0f172a',metadata={'Software':None}); print('docs/og.png')
