I18N_ADD({'zh-CN':{title:'Awesome Local Inference Recipes · 本地推理配方',eb:'本地推理配方：模型 × 引擎 × 硬件，每个数字都有出处。',h1:'同一张卡，换个配方<br><span>速度差 10 倍</span>',
 lead:'收集社区里真实跑出来的本地推理配方：哪个模型、什么量化、哪个引擎、什么硬件，跑出多少 tok/s、花多少钱。',
 p1:'🔀 跨引擎：Strata · oMLX · DFlash2 · TensorFold · llama.cpp',p2:'🖥️ 消费级 / 二手硬件',p3:'🔗 每个数字标来源',p4:'💰 聚焦 ≤ $30k',cta1:'浏览配方库 →',cta2:'提交你的配方',
 hot:'🔥 X 上的热门配方 <small>按点赞+转发排序 · 点击查看原帖</small>',bud:'按预算进入',t1:'二手 3090 / 4090、MI50、V100、Strix Halo',t2:'单张 5090、单台 DGX Spark、Mac Studio Max',t3:'双 Spark、Mac Studio M5 Ultra',t4:'3–4 台 Spark 集群、多卡工作站',
 lvh:'来源等级怎么看',l_off:'官方',l_mea:'实测',l_rel:'转述',l_cla:'宣称',d_off:'项目方或厂商发布的数字，通常是最佳条件。',d_mea:'作者本人在自己的机器上跑出来，附截图或日志。',d_rel:'二手引用别人的结果，需要回原帖核对。',d_cla:'预测值或无复现条件，仅供参考。',
 note:'未知字段统一显示「未见公开数据」，不估算、不补数。',fh:'你跑过一个好配方？',fp:'一条 JSON，一个 PR，就能让下一个人少折腾一周。',
 foot:'Awesome Local Inference Recipes · 数据整理自 X / GitHub / Reddit / 价格站',footd:' · 最新条目 {d}',k1:'条配方',k2:'种引擎',k3:'类硬件',k4:'带来源链接',k5:'条实测'},
 en:{title:'Awesome Local Inference Recipes',eb:'Local inference recipes: model × engine × hardware, every number sourced.',h1:'Same GPU, different recipe<br><span>10× the speed</span>',
 lead:'Real local inference setups collected from the community: which model, which quant, which engine, which hardware, how many tok/s and what it costs.',
 p1:'🔀 Cross-engine: Strata · oMLX · DFlash2 · TensorFold · llama.cpp',p2:'🖥️ Consumer / used hardware',p3:'🔗 Every number has a source',p4:'💰 Focus on ≤ $30k',cta1:'Explore recipes →',cta2:'Submit your recipe',
 hot:'🔥 Popular recipes on X <small>by likes + reposts · click to open the post</small>',bud:'Browse by budget',t1:'Used 3090 / 4090, MI50, V100, Strix Halo',t2:'Single 5090, one DGX Spark, Mac Studio Max',t3:'Two Sparks, Mac Studio M5 Ultra',t4:'3–4 Spark cluster, multi-GPU workstation',
 lvh:'What the source levels mean',l_off:'Official',l_mea:'Measured',l_rel:'Relayed',l_cla:'Claimed',d_off:'Numbers published by the project or vendor, usually best-case.',d_mea:'The author ran it on their own machine, with a screenshot or log.',d_rel:'A second-hand quote of someone else’s result; check the original post.',d_cla:'A prediction or no reproduction details; for reference only.',
 note:'Unknown fields always show “no public data”. Nothing is estimated or filled in.',fh:'Ran a great recipe?',fp:'One JSON entry, one PR, and the next person saves a week of tinkering.',
 foot:'Awesome Local Inference Recipes · compiled from X / GitHub / Reddit / price sites',footd:' · newest entry {d}',k1:'recipes',k2:'engines',k3:'hardware types',k4:'with source link',k5:'measured'}});
applyI18n();
fetch('data/recipes.json').then(r=>r.json()).then(D=>{
const e=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const hot=D.filter(r=>r.x_post).sort((a,b)=>(b.x_post.likes+3*b.x_post.reposts)-(a.x_post.likes+3*a.x_post.reposts)).slice(0,9);
document.getElementById('hot').innerHTML=hot.map(r=>`<a class="hc" href="${e(r.source_url)}" target="_blank" rel="noopener">
<div class="hm"><span class="lv ${r.source_level}">${TL(r.source_level)}</span><span>♥ ${r.x_post.likes} · ⟲ ${r.x_post.reposts}</span></div>
<div class="big">${r.tok_s!=null?r.tok_s+'<small> tok/s</small>':'🎬'}</div><b>${e(r.model)}</b>
<div class="sub">${e(r.engine)} · ${e(r.quant||'')}</div><div class="sub">${e(r.hardware)}</div>
<div class="mt">${e(r.metric)}</div><div class="au">@${e(r.x_post.author)}${r.date?' · '+e(r.date):''}</div></a>`).join('');
const n=(f)=>D.filter(f).length;
document.getElementById('ks').innerHTML=[[D.length,T('k1')],[new Set(D.map(r=>r.engine.split(/[ （]/)[0])).size,T('k2')],[new Set(D.map(r=>r.hardware_family)).size,T('k3')],[Math.round(100*n(r=>r.source_url)/D.length)+'%',T('k4')],[n(r=>r.source_level=='实测'),T('k5')]].map(([a,b])=>`<div class="k"><b>${a}</b>${b}</div>`).join('');
const nd=D.map(r=>r.date).filter(Boolean).sort().pop();if(nd)document.querySelector('footer').textContent=T('foot')+T('footd',{d:nd});
});
