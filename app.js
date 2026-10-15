I18N_ADD({'zh-CN':{title:'配方库 · 本地推理配方',xh1:'什么模型 × 什么硬件 × 什么引擎 = 多快、多贵',xlead:'聚焦 3 万美元以内的本地推理方案。每条数据附来源与可信等级，未知字段一律显示「未见公开数据」。',
 ph:'搜索模型 / 硬件 / 引擎 / 量化…',allcat:'全部类别',c_text:'文字',c_image:'图像',c_va:'影音',alleng:'全部引擎',allmf:'全部模型系列',allhw:'全部硬件',alllv:'全部来源等级',
 l_off:'官方',l_mea:'实测',l_rel:'转述',l_cla:'宣称',budget:'预算 ≤',unk:'含成本未知',chh:'tok/s vs 硬件成本（文字模型，两项均已知）',lgh:'说明',
 lg1:'<b>美元/tok/s</b> = 硬件成本 ÷ 单流 tok/s，越低越划算',lg2:'成本取来源区间下限；多卡按张计价的行不自动折算（显示原文）',lg3:'来源等级：',lg4:'点击任意行查看详情、启动命令和来源',lg5:'指标原文、硬件等字段保留来源原文',
 th_cat:'类别',th_model:'模型',th_quant:'量化/优化',th_eng:'引擎',th_hw:'硬件',th_metric:'指标原文',th_cost:'成本 $',th_ctx:'上下文',th_src:'来源',
 xfoot:'数据来自 X / GitHub / Reddit / 价格站整理',xfootd:'，最新条目 {d}',tags:'标签',st_all:'配方',st_text:'文字',st_img:'图像',st_va:'影音',st_cmd:'含启动命令',
 count:'共 {n} 条（总 {t}）',xaxis:'硬件成本 (USD)',empty:'当前筛选无可绘制数据',d_quant:'量化/优化',d_mf:'模型系列',d_tags:'标签',d_eng:'引擎',d_orig:'原文：',d_hw:'硬件',d_perf:'性能',d_tok:'单流 tok/s',d_conc:'并发',d_ctx:'上下文',d_cost:'硬件成本',d_date:'日期',d_note:'来源说明',
 d_cmd:'启动命令',d_nocmd:'# 未见公开数据\n# 你跑过这个配置？欢迎提交 PR 补全启动命令',d_src:'来源',d_guide:'📘 运行指南',d_fix:'✎ 提交修正 / 补充',d_sup:'已被 {id} 取代'},
 en:{title:'Explore · Awesome Local Inference Recipes',xh1:'Which model × which hardware × which engine = how fast, how much',xlead:'Local inference setups under $30k. Every row carries a source and a trust level; unknown fields show “no public data”.',
 ph:'Search model / hardware / engine / quant…',allcat:'All categories',c_text:'Text',c_image:'Image',c_va:'Video & audio',alleng:'All engines',allmf:'All model families',allhw:'All hardware',alllv:'All source levels',
 l_off:'Official',l_mea:'Measured',l_rel:'Relayed',l_cla:'Claimed',budget:'Budget ≤',unk:'Include unknown cost',chh:'tok/s vs hardware cost (text models with both known)',lgh:'Notes',
 lg1:'<b>$/tok/s</b> = hardware cost ÷ single-stream tok/s; lower is better value',lg2:'Cost is the low end of the quoted range; per-card prices for multi-GPU rows are not multiplied (original text shown)',lg3:'Source levels: ',lg4:'Click any row for details, launch command and source',lg5:'Metric shows an English version where one exists (hover for the original); hardware and other fields keep the source’s wording',
 th_cat:'Type',th_model:'Model',th_quant:'Quant / opt.',th_eng:'Engine',th_hw:'Hardware',th_metric:'Metric',th_cost:'Cost $',th_ctx:'Context',th_src:'Source',
 xfoot:'Compiled from X / GitHub / Reddit / price sites',xfootd:' · newest entry {d}',tags:'Tags',st_all:'recipes',st_text:'text',st_img:'image',st_va:'video & audio',st_cmd:'with launch command',
 count:'{n} shown ({t} total)',xaxis:'Hardware cost (USD)',empty:'Nothing to plot for this filter',d_quant:'Quant / optimization',d_mf:'Model family',d_tags:'Tags',d_eng:'Engine',d_orig:'original: ',d_hw:'Hardware',d_perf:'Performance',d_tok:'Single-stream tok/s',d_conc:'Concurrency',d_ctx:'Context',d_cost:'Hardware cost',d_date:'Date',d_note:'Source note',
 d_cmd:'Launch command',d_nocmd:'# no public data\n# Ran this setup? Send a PR with the launch command',d_src:'Source',d_guide:'📘 How-to guide',d_fix:'✎ Submit a fix / addition',d_sup:'superseded by {id}'}});
applyI18n();
let GUIDES=new Set();const GP=fetch('data/guides.json').then(r=>r.ok?r.json():[]).then(a=>{GUIDES=new Set(a)}).catch(()=>{});
const MET=r=>LANG=='en'&&r.metric_en?r.metric_en:r.metric;
const NA=`<span class="na">${T('na')}</span>`,CAT={text:TC('text'),image:TC('image'),'video-audio':TC('video-audio')};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const v=x=>x==null||x===''?NA:esc(x);let D=[],sk='tok_s',sd=-1;const $=id=>document.getElementById(id);
const COL={'官方':'#4f46e5','实测':'#16a34a','转述':'#d97706','宣称':'#dc2626'};
fetch('data/recipes.json').then(r=>r.json()).then(d=>{D=d.map(r=>({...r,cpt:r.tok_s&&r.hardware_cost_usd?Math.round(r.hardware_cost_usd/r.tok_s):null}));
 const cnt=k=>{const c={};D.forEach(r=>c[r[k]]=(c[r[k]]||0)+1);return Object.entries(c).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]))};
 for(const [id,k] of [['eng','engine'],['mf','model_family'],['fam','hardware_family']])cnt(k).forEach(([x,n])=>$(id).add(new Option(`${k=='hardware_family'?TF(x):x} (${n})`,x)));
 const tc={};D.forEach(r=>r.tags.forEach(t=>tc[t]=(tc[t]||0)+1));
 $('chips').innerHTML=`<span class="cl">${T('tags')}</span>`+Object.entries(tc).sort((a,b)=>b[1]-a[1]).map(([t,n])=>`<button class="chip" data-t="${esc(t)}">${esc(t)} <i>${n}</i></button>`).join('');
 $('chips').querySelectorAll('.chip').forEach(b=>b.onclick=()=>toggleTag(b.dataset.t));
 $('stats').innerHTML=[[T('st_all'),D.length],[T('st_text'),D.filter(r=>r.category=='text').length],[T('st_img'),D.filter(r=>r.category=='image').length],[T('st_va'),D.filter(r=>r.category=='video-audio').length],[T('st_cmd'),D.filter(r=>r.launch_command).length]].map(([a,b])=>`<div class="stat"><b>${b}</b>${a}</div>`).join('');
 const id=applyParams();render();if(id&&D.some(r=>r.id==id))GP.then(()=>open(id));
 const nd=D.map(r=>r.date).filter(Boolean).sort().pop();if(nd)document.getElementById('xd').textContent=T('xfootd',{d:nd});});
let TG=new Set();function toggleTag(t){TG.has(t)?TG.delete(t):TG.add(t);render()}
['q','cat','eng','mf','fam','lvl','budget','unk'].forEach(i=>$(i).addEventListener('input',render));
function sync(){const P=new URLSearchParams();const m={q:'q',cat:'cat',eng:'engine',mf:'family',fam:'fam',lvl:'level'};
 for(const [id,k] of Object.entries(m))if($(id).value)P.set(k,$(id).value);if(+$('budget').value<30000)P.set('max',$('budget').value);if(TG.size)P.set('tag',[...TG].join(','));
 const lg=new URLSearchParams(location.search).get('lang');if(lg)P.set('lang',lg);
 history.replaceState(null,'',location.pathname+(P.toString()?'?'+P:''));
 document.querySelectorAll('.chip').forEach(b=>b.classList.toggle('on',TG.has(b.dataset.t)));}
document.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;sd=sk==k?-sd:1;sk=k;render()});
function filt(){const q=$('q').value.toLowerCase(),b=+$('budget').value;$('bv').textContent='$'+b.toLocaleString();
 return D.filter(r=>(!q||[r.model,r.quant,r.engine,r.engine_note,r.hardware,r.metric,r.metric_en,r.model_family,...r.tags].join(' ').toLowerCase().includes(q))&&(!$('cat').value||r.category==$('cat').value)&&(!$('eng').value||r.engine==$('eng').value)&&(!$('fam').value||r.hardware_family==$('fam').value)&&(!$('mf').value||r.model_family==$('mf').value)&&[...TG].every(t=>r.tags.includes(t))&&(!$('lvl').value||r.source_level==$('lvl').value)&&(r.hardware_cost_usd==null?$('unk').checked:r.hardware_cost_usd<=b));}
function render(){if(D.length)sync();const L=filt().sort((a,b)=>{const x=a[sk],y=b[sk];if(x==null)return 1;if(y==null)return -1;return (x>y?1:x<y?-1:0)*sd});
 document.querySelectorAll('th').forEach(t=>{t.classList.toggle('s',t.dataset.k==sk);t.classList.toggle('d',sd<0)});
 $('count').textContent=T('count',{n:L.length,t:D.length});
 $('tb').innerHTML=L.map(r=>`<tr data-id="${r.id}"><td><span class="tag">${CAT[r.category]}</span></td><td><b>${esc(r.model)}</b><br><span class="tag fam">${esc(r.model_family)}</span>${r.tags.map(t=>`<span class="tg" data-t="${esc(t)}">${esc(t)}</span>`).join('')}</td><td>${v(r.quant)}</td><td>${esc(r.engine)}${r.engine_note?`<br><small class="na">${esc(r.engine_note)}</small>`:''}</td><td>${esc(r.hardware)}<br><span class="tag">${esc(TF(r.hardware_family))}</span></td><td class="n">${v(r.tok_s)}</td><td${MET(r)!==r.metric?` title="${esc(r.metric)}"`:''}>${v(MET(r))}</td><td class="n">${r.hardware_cost_usd!=null?r.hardware_cost_usd.toLocaleString():v(r.hardware_cost_text)}</td><td class="n">${v(r.cpt)}</td><td>${v(r.context)}</td><td><span class="lv ${r.source_level}">${TL(r.source_level)}</span></td></tr>`).join('');
 document.querySelectorAll('#tb tr').forEach(tr=>tr.onclick=()=>open(tr.dataset.id));document.querySelectorAll('#tb .tg').forEach(g=>g.onclick=e=>{e.stopPropagation();toggleTag(g.dataset.t)});chart(L);}
function chart(L){const P=L.filter(r=>r.tok_s&&r.hardware_cost_usd),W=640,H=300,m={l:50,r:15,t:10,b:36};
 const xm=Math.max(30000,...P.map(p=>p.hardware_cost_usd)),ym=Math.max(50,...P.map(p=>p.tok_s))*1.08;
 const X=c=>m.l+c/xm*(W-m.l-m.r),Y=t=>H-m.b-t/ym*(H-m.t-m.b);let s='';
 for(let i=0;i<=6;i++){const c=xm*i/6;s+=`<line x1="${X(c)}" x2="${X(c)}" y1="${m.t}" y2="${H-m.b}" stroke="#eef0f5"/><text x="${X(c)}" y="${H-m.b+16}" font-size="10" text-anchor="middle" fill="#889">$${Math.round(c/1000)}k</text>`}
 for(let i=0;i<=5;i++){const t=ym*i/5;s+=`<line x1="${m.l}" x2="${W-m.r}" y1="${Y(t)}" y2="${Y(t)}" stroke="#eef0f5"/><text x="${m.l-6}" y="${Y(t)+3}" font-size="10" text-anchor="end" fill="#889">${Math.round(t)}</text>`}
 s+=`<text x="${W/2}" y="${H-4}" font-size="11" text-anchor="middle" fill="#556">${T('xaxis')}</text><text x="12" y="${H/2}" font-size="11" fill="#556" transform="rotate(-90 12 ${H/2})" text-anchor="middle">tok/s</text>`;
 s+=P.map(p=>`<circle class="dot" data-id="${p.id}" cx="${X(p.hardware_cost_usd)}" cy="${Y(p.tok_s)}" r="5" fill="${COL[p.source_level]}" fill-opacity=".7"><title>${esc(p.model)} · ${esc(p.hardware)} · ${p.tok_s} tok/s · $${p.hardware_cost_usd}</title></circle>`).join('');
 s+=Object.entries(COL).map(([k,c],i)=>`<circle cx="${W-(LANG=='en'?300:180)+i*(LANG=='en'?74:44)}" cy="16" r="5" fill="${c}"/><text x="${W-(LANG=='en'?292:172)+i*(LANG=='en'?74:44)}" y="20" font-size="11" fill="#556">${TL(k)}</text>`).join('');
 $('chart').innerHTML=s+(P.length?'':`<text x="320" y="150" text-anchor="middle" fill="#99a">${T('empty')}</text>`);
 document.querySelectorAll('.dot').forEach(d=>d.onclick=()=>open(d.dataset.id));}
function open(id){const r=D.find(x=>x.id==id);$('dc').innerHTML=`<h2 style="margin-top:0">${esc(r.model)}</h2><p><span class="tag">${CAT[r.category]}</span> <span class="lv ${r.source_level}">${TL(r.source_level)}</span> <span class="tag">${r.id}</span>${r.superseded_by?` <span class="tag">${T('d_sup',{id:esc(r.superseded_by)})}</span>`:''}</p>
<dl><dt>${T('d_quant')}</dt><dd>${v(r.quant)}</dd><dt>${T('d_mf')}</dt><dd>${esc(r.model_family)}</dd><dt>${T('d_tags')}</dt><dd>${r.tags.map(t=>`<span class="tg">${esc(t)}</span>`).join('')||'—'}</dd><dt>${T('d_eng')}</dt><dd>${esc(r.engine)}${r.engine_note?` (${T('d_orig')}${esc(r.engine_note)})`:''}</dd><dt>${T('d_hw')}</dt><dd>${esc(r.hardware)} (${esc(TF(r.hardware_family))})</dd><dt>${T('d_perf')}</dt><dd>${v(MET(r))}${MET(r)!==r.metric?`<br><small class="na">${T('d_orig')}${esc(r.metric)}</small>`:''}</dd><dt>${T('d_tok')}</dt><dd>${v(r.tok_s)}</dd><dt>${T('d_conc')}</dt><dd>${v(r.concurrency)}</dd><dt>${T('d_ctx')}</dt><dd>${v(r.context)}</dd><dt>${T('d_cost')}</dt><dd>${v(r.hardware_cost_text)}</dd><dt>$/tok/s</dt><dd>${v(r.cpt)}</dd><dt>${T('d_date')}</dt><dd>${v(r.date)}</dd><dt>${T('d_note')}</dt><dd>${v(r.source_note)}</dd></dl>
<h3>${T('d_cmd')}</h3>${r.launch_command?`<pre>${esc(r.launch_command)}</pre>`:`<pre>${esc(T('d_nocmd'))}</pre>`}
<h3>${T('d_src')}</h3><p><a href="${esc(r.source_url)}" target="_blank" rel="noopener">${esc(r.source_url)}</a></p>${GUIDES.has(r.id)?`<p><a href="https://github.com/raytone-lab/Awesome-local-inference-recipe/blob/main/recipes/${esc(r.id)}${LANG=='zh-CN'?'.zh-CN':''}.md" target="_blank" rel="noopener">${T('d_guide')}</a></p>`:""}<p><a href="submit.html">${T('d_fix')}</a></p>`;
 $('drawer').classList.add('open');$('mask').classList.add('open');}
$('x').onclick=$('mask').onclick=()=>{$('drawer').classList.remove('open');$('mask').classList.remove('open')};
// deep-link: explore.html?family=Qwen&tag=MoE,4bit&engine=llama.cpp&fam=Mac&cat=text&level=实测&max=3000&q=...
function applyParams(){const U=new URLSearchParams(location.search);if(U.get('max'))$('budget').value=U.get('max');
 for(const [id,k] of [['fam','fam'],['mf','family'],['eng','engine'],['cat','cat'],['lvl','level']])if(U.get(k))$(id).value=U.get(k);
 if(U.get('tag'))U.get('tag').split(',').filter(Boolean).forEach(t=>TG.add(t));if(U.get('q'))$('q').value=U.get('q');
 return U.get('id');}
