I18N_ADD({'zh-CN':{title:'Awesome Local Inference Recipes · 本地推理配方',eb:'开放数据集 · 模型 × 引擎 × 硬件 · 每个数字都有出处',h1:'同一张卡，换个配方<br><span>速度差 10 倍</span>',
 lead:'你手上的（或准备买的）硬件，用哪个模型、什么量化、哪个引擎能跑出最多 tok/s，要花多少钱。每个数字都链接到原始出处。',
 cta1:'浏览配方库 →',cta2:'提交你的配方',cta3:'我的机器能跑什么？→',cta_note:'免费开放数据（CC BY 4.0），点个 Star 能让更多人找到它。',
 tbh:'各预算档最快的实测配置',tbs:'文字模型 · 单流',tball:'查看全部实测配方 →',k_gpu:'独立显卡（仅卡价）',k_sys:'整机',k_al:'价格口径',pr_gpu:'显卡',pr_sys:'整机',tbn:'独立显卡只计显卡价格，不含主机其余部分；各行模型不同，速度不能直接横比。',
 v1h:'🔗 每个数字都有出处',v1:'每一行都链接到原帖、README 或日志，并标注可信等级：官方、实测、转述、宣称。',v2h:'🔀 跨引擎对比',v2:'llama.cpp、MLX、vLLM、SGLang、Strata、oMLX、DFlash、TensorFold……在同一硬件上对比。',
 v3h:'🖥️ 买得到的硬件',v3:'消费级显卡、Mac、DGX Spark、Strix Halo、二手数据中心卡，全部 3 万美元以内。',v4h:'🚫 不估算',v4:'未知字段一律显示「未见公开数据」，不估算、不补数。',
 bvh:'性价比最高的实测配置',bvs:'每 tok/s 单流速度对应的硬件成本最低（有价格的实测文字配方），显卡价与整机价分开排名。',bvall:'查看完整排名 →',per:'美元 / tok/s',bvn:'<b>独立显卡的价格只含显卡</b>，不含 CPU、内存、主板等；整机价（Mac、DGX Spark、迷你主机）是整台机器。每一行跑的是不同模型（参数量、量化各异），tok/s 不是同一任务下的对比。',bvg:'独立显卡 · 仅显卡价格',bvs2:'整机 · Mac、DGX Spark、迷你主机',
 spe:'交互演示',sph:'每秒 10、50、500 个 token 到底是什么感觉？',spp:'同一段回答按不同速度流式输出，对照人的阅读速度和真实实测配置。',spb:'打开速度体感演示 →',
 mini:'本地推理配方把模型、量化、引擎和硬件放在一起比较：同一张显卡换一个引擎或量化方式，单流速度可能相差十倍，而每个数字都附上原始来源链接，方便你自己核对。',
 hot:'🔥 X 上的热门配方',hots:'按点赞 + 转发 ×3 加权排序，点击卡片查看原帖。',al_props:'特点',bud:'按预算浏览',t1:'二手 3090 / 4090、MI50、V100、Strix Halo',t2:'单张 5090、单台 DGX Spark、Mac Studio Max',t3:'双 Spark、Mac Studio M5 Ultra',t4:'3–4 台 Spark 集群、多卡工作站',
 lvh:'来源等级怎么看',l_off:'官方',l_mea:'实测',l_rel:'转述',l_cla:'宣称',d_off:'项目方或厂商发布的数字，通常是最佳条件。',d_mea:'作者本人在自己的机器上跑出来，附截图或日志。',d_rel:'二手引用别人的结果，需要回原帖核对。',d_cla:'预测值或无复现条件，仅供参考。',
 fh:'帮你省了一周的折腾？',fp:'点个 Star 让下一个人也能找到它；或者把你跑过的配方加进来：一条 JSON，一个 PR。',
 footd:' · 最新条目 {d}',k1:'条配方',k2:'种引擎',k3:'类硬件',k4:'带来源链接',k5:'条实测',k6:'最新条目'},
 en:{title:'Awesome Local Inference Recipes',eb:'Open dataset · model × engine × hardware · every number sourced',h1:'Same GPU, different recipe<br><span>10× the speed</span>',
 lead:'Find out which model, quant and engine gets the most tok/s out of the hardware you have or plan to buy, and what it costs. Every number links to its source.',
 cta1:'Explore recipes →',cta2:'Submit your recipe',cta3:'What can my machine run? →',cta_note:'Free, open data (CC BY 4.0). A star helps other people find it.',
 tbh:'Fastest measured setup per budget',tbs:'text models · single stream',tball:'All measured recipes →',k_gpu:'Discrete GPUs (card only)',k_sys:'Whole systems',k_al:'Price basis',pr_gpu:'card',pr_sys:'system',tbn:'Discrete-card prices are GPU-only, not the whole PC. Each row is a different model, so speeds aren’t directly comparable.',
 v1h:'🔗 Every number has a source',v1:'Each row links to the post, README or log it came from, with a trust level: official, measured, relayed or claimed.',v2h:'🔀 Cross-engine',v2:'llama.cpp, MLX, vLLM, SGLang, Strata, oMLX, DFlash, TensorFold… compared on the same hardware.',
 v3h:'🖥️ Hardware you can buy',v3:'Consumer GPUs, Macs, DGX Spark, Strix Halo and used datacenter cards, all under $30k.',v4h:'🚫 No estimates',v4:'Unknown fields say “no public data”. Nothing is estimated or filled in.',
 bvh:'Best value measured setups',bvs:'Lowest hardware cost per single-stream tok/s (measured text recipes with a known price), ranked separately for card prices and whole-system prices.',bvall:'See the full ranking →',per:'$ per tok/s',bvn:'<b>Prices are GPU-only for discrete cards</b>: CPU, RAM and the rest of the PC are not included. Whole-system prices (Mac, DGX Spark, mini PCs) cover the entire machine. Every row runs a different model (size and quant vary), so tok/s is not a like-for-like comparison.',bvg:'Discrete GPUs · card price only',bvs2:'Whole systems · Mac, DGX Spark, mini PCs',
 spe:'Interactive demo',sph:'What do 10, 50 and 500 tok/s actually feel like?',spp:'Watch the same answer stream at different speeds, next to human reading pace and real measured setups.',spb:'Open the speed demo →',
 mini:'Local inference recipes compare model, quant, engine and hardware side by side: on the same GPU, a different engine or quant can change single-stream speed by ten times, and every number carries a link to its source so you can check it yourself.',
 hot:'🔥 Popular on X',hots:'Ranked by likes + reposts (reposts weighted ×3). Click a card to open the original post.',al_props:'Why this list',bud:'Browse by budget',t1:'Used 3090 / 4090, MI50, V100, Strix Halo',t2:'Single 5090, one DGX Spark, Mac Studio Max',t3:'Two Sparks, Mac Studio M5 Ultra',t4:'3–4 Spark cluster, multi-GPU workstation',
 lvh:'What the source levels mean',l_off:'Official',l_mea:'Measured',l_rel:'Relayed',l_cla:'Claimed',d_off:'Numbers published by the project or vendor, usually best-case.',d_mea:'The author ran it on their own machine, with a screenshot or log.',d_rel:'A second-hand quote of someone else’s result; check the original post.',d_cla:'A prediction or no reproduction details; for reference only.',
 fh:'Saved you a week of tinkering?',fp:'Star the repo so the next person finds it, or add the recipe you ran: one JSON entry, one PR.',
 footd:' · newest entry {d}',k1:'recipes',k2:'engines',k3:'hardware types',k4:'with source link',k5:'measured',k6:'newest entry'}});
applyI18n();
const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const MEA='实测',$=id=>document.getElementById(id),k$=n=>n>=1000?'$'+(n/1000).toFixed(n%1000?1:0).replace(/\.0$/,'')+'k':'$'+n;
const xl=id=>'explore.html?id='+encodeURIComponent(id);
// mini speed lanes: the same text revealed at 10 / 50 / 500 tok/s (≈4 chars per token in English, ≈1.4 per CJK char); loops every 7 s
(function(){const el=$('mini'),txt=T('mini'),cpt=LANG=='en'?4:1.4,R=[10,50,500];
 el.innerHTML=R.map(r=>`<div class="ml"><div class="mh"><b>${r} tok/s</b><span></span></div><div class="mt"></div></div>`).join('');
 const L=[...el.querySelectorAll('.ml')];if(matchMedia('(prefers-reduced-motion: reduce)').matches){L.forEach((l,i)=>l.querySelector('.mt').textContent=txt.slice(0,Math.round(R[i]*3*cpt)));return}
 // paused while scrolled offscreen or the tab is hidden; resumes where it stopped
 let t0=performance.now(),raf=0,paused=0,vis=true;const f=now=>{let s=(now-t0)/1000;if(s>7){t0=now;s=0}
  L.forEach((l,i)=>{const n=Math.min(txt.length,Math.floor(s*R[i]*cpt));const m=l.querySelector('.mt');if(m.textContent.length!==n){m.textContent=txt.slice(0,n);m.scrollTop=m.scrollHeight}l.querySelector('.mh span').textContent=s.toFixed(1)+' s'});raf=requestAnimationFrame(f)};
 const run=()=>{const on=vis&&!document.hidden;if(on&&!raf){if(paused)t0+=performance.now()-paused;paused=0;raf=requestAnimationFrame(f)}else if(!on&&raf){cancelAnimationFrame(raf);raf=0;paused=performance.now()}};
 if('IntersectionObserver' in window)new IntersectionObserver(es=>{vis=es[es.length-1].isIntersecting;run()}).observe(el);
 document.addEventListener('visibilitychange',run);run()})();
fetch('data/recipes.json').then(r=>r.json()).then(D=>{
 const n=f=>D.filter(f).length,nd=D.map(r=>r.date).filter(Boolean).sort().pop();
 $('ks').innerHTML=[[D.length,T('k1')],[new Set(D.map(r=>r.engine.split(/[ （]/)[0])).size,T('k2')],[n(r=>r.source_level==MEA),T('k5')],...(nd?[[nd,T('k6')]]:[])].map(([a,b])=>`<div class="k"><b>${e(a)}</b>${e(b)}</div>`).join('');
 // like-for-like only: card-only and whole-system prices are ranked separately (costKind, cost.js); self-reported (自称) rows are left out
 const M=D.filter(r=>r.category=='text'&&r.source_level==MEA&&!selfReported(r)&&r.tok_s&&r.hardware_cost_usd&&!r.superseded_by).map(r=>({...r,kind:costKind(r)}));
 const B={gpu:[[0,1000],[1000,2500],[2500,7000],[7000,30000]],sys:[[0,2500],[2500,7000],[7000,14000],[14000,30000]]};
 const bands=k=>B[k].map(([lo,hi])=>{const x=M.filter(r=>r.kind==k&&r.hardware_cost_usd>lo&&r.hardware_cost_usd<=hi).sort((a,b)=>b.tok_s-a.tok_s)[0];
  const lab=lo?`${k$(lo)}–${k$(hi).slice(1)}`:`≤ ${k$(hi)}`;
  return x?`<li><a href="${xl(x.id)}"><span class="bt">${lab}</span><span class="m">${e(x.model)}<span class="h">${e(x.hardware)} · ${e(x.engine)}</span></span><span class="v">${e(x.tok_s)}<small>tok/s</small></span></a></li>`:''}).join('');
 const tabs=[...document.querySelectorAll('#tbk [role=tab]')],sel=b=>{tabs.forEach(t=>{const on=t===b;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1});$('tb').innerHTML=bands(b.dataset.k);$('tb').setAttribute('aria-labelledby',b.id)};
 tabs.forEach((b,i)=>{b.onclick=()=>sel(b);b.onkeydown=ev=>{const d={ArrowRight:1,ArrowLeft:-1}[ev.key];if(d){const t=tabs[(i+d+tabs.length)%tabs.length];sel(t);t.focus()}}});sel(tabs[0]);
 for(const k of ['gpu','sys']){const seen=new Set(),bv=M.filter(r=>r.kind==k).map(r=>({...r,cpt:r.hardware_cost_usd/r.tok_s})).sort((a,b)=>a.cpt-b.cpt).filter(r=>{const q=r.model+'|'+r.hardware;if(seen.has(q))return false;seen.add(q);return true}).slice(0,3);
 $('bv-'+k).innerHTML=bv.map((r,i)=>`<a class="bvc" href="${xl(r.id)}"><div class="r1"><span class="cpt">$${Math.round(r.cpt)}<small> / tok/s</small></span><span class="rank">#${i+1}</span></div>
<b class="m">${e(r.model)}</b><span class="s">${e(r.hardware)}</span><span class="s">${e(r.engine)}${r.quant?' · '+e(r.quant):''}</span>
<div class="nums"><span><b>${e(r.tok_s)}</b> tok/s</span><span><b>$${r.hardware_cost_usd.toLocaleString()}</b> <small>${T('pr_'+k)}</small></span></div></a>`).join('')}
 const hot=D.filter(r=>r.x_post).sort((a,b)=>(b.x_post.likes+3*b.x_post.reposts)-(a.x_post.likes+3*a.x_post.reposts)).slice(0,6);
 $('hot').innerHTML=hot.map(r=>`<a class="hc" href="${e(r.source_url)}" target="_blank" rel="noopener">
<div class="hm"><span class="lv ${e(r.source_level)}">${e(TL(r.source_level))}</span><span>♥ ${e(r.x_post.likes)} · ⟲ ${e(r.x_post.reposts)}</span></div>
<div class="big">${r.tok_s!=null?e(r.tok_s)+'<small> tok/s</small>':'🎬'}</div><b>${e(r.model)}</b>
<div class="sub">${e(r.engine)}${r.quant?' · '+e(r.quant):''}</div><div class="sub">${e(r.hardware)}</div>
<div class="mt">${e(LANG=='en'&&r.metric_en?r.metric_en:r.metric)}</div><div class="au">@${e(r.x_post.author)}${r.date?' · '+e(r.date):''}</div></a>`).join('');
 if(nd)$('xd').textContent=T('footd',{d:nd});
});
