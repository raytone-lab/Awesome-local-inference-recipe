const NA='<span class="na">未见公开数据</span>',CAT={text:'文字',image:'图像','video-audio':'影音'};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const v=x=>x==null||x===''?NA:esc(x);let D=[],sk='tok_s',sd=-1;const $=id=>document.getElementById(id);
const COL={'官方':'#4f46e5','实测':'#16a34a','转述':'#d97706','宣称':'#dc2626'};
fetch('data/recipes.json').then(r=>r.json()).then(d=>{D=d.map(r=>({...r,cpt:r.tok_s&&r.hardware_cost_usd?Math.round(r.hardware_cost_usd/r.tok_s):null}));
 for(const [id,k] of [['eng','engine'],['fam','hardware_family']])[...new Set(D.map(r=>r[k]))].sort().forEach(x=>$(id).add(new Option(x,x)));
 $('stats').innerHTML=[['配方',D.length],['文字',D.filter(r=>r.category=='text').length],['图像',D.filter(r=>r.category=='image').length],['影音',D.filter(r=>r.category=='video-audio').length],['含启动命令',D.filter(r=>r.launch_command).length]].map(([a,b])=>`<div class="stat"><b>${b}</b>${a}</div>`).join('');
 render();});
['q','cat','eng','fam','lvl','budget','unk'].forEach(i=>$(i).addEventListener('input',render));
document.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;sd=sk==k?-sd:1;sk=k;render()});
function filt(){const q=$('q').value.toLowerCase(),b=+$('budget').value;$('bv').textContent='$'+b.toLocaleString();
 return D.filter(r=>(!q||[r.model,r.quant,r.engine,r.hardware,r.metric].join(' ').toLowerCase().includes(q))&&(!$('cat').value||r.category==$('cat').value)&&(!$('eng').value||r.engine==$('eng').value)&&(!$('fam').value||r.hardware_family==$('fam').value)&&(!$('lvl').value||r.source_level==$('lvl').value)&&(r.hardware_cost_usd==null?$('unk').checked:r.hardware_cost_usd<=b));}
function render(){const L=filt().sort((a,b)=>{const x=a[sk],y=b[sk];if(x==null)return 1;if(y==null)return -1;return (x>y?1:x<y?-1:0)*sd});
 document.querySelectorAll('th').forEach(t=>{t.classList.toggle('s',t.dataset.k==sk);t.classList.toggle('d',sd<0)});
 $('count').textContent=`共 ${L.length} 条（总 ${D.length}）`;
 $('tb').innerHTML=L.map(r=>`<tr data-id="${r.id}"><td><span class="tag">${CAT[r.category]}</span></td><td><b>${esc(r.model)}</b></td><td>${v(r.quant)}</td><td>${esc(r.engine)}</td><td>${esc(r.hardware)}<br><span class="tag">${r.hardware_family}</span></td><td class="n">${v(r.tok_s)}</td><td>${v(r.metric)}</td><td class="n">${r.hardware_cost_usd!=null?r.hardware_cost_usd.toLocaleString():v(r.hardware_cost_text)}</td><td class="n">${v(r.cpt)}</td><td>${v(r.context)}</td><td><span class="lv ${r.source_level}">${r.source_level}</span></td></tr>`).join('');
 document.querySelectorAll('#tb tr').forEach(tr=>tr.onclick=()=>open(tr.dataset.id));chart(L);}
function chart(L){const P=L.filter(r=>r.tok_s&&r.hardware_cost_usd),W=640,H=300,m={l:50,r:15,t:10,b:36};
 const xm=Math.max(30000,...P.map(p=>p.hardware_cost_usd)),ym=Math.max(50,...P.map(p=>p.tok_s))*1.08;
 const X=c=>m.l+c/xm*(W-m.l-m.r),Y=t=>H-m.b-t/ym*(H-m.t-m.b);let s='';
 for(let i=0;i<=6;i++){const c=xm*i/6;s+=`<line x1="${X(c)}" x2="${X(c)}" y1="${m.t}" y2="${H-m.b}" stroke="#eef0f5"/><text x="${X(c)}" y="${H-m.b+16}" font-size="10" text-anchor="middle" fill="#889">$${Math.round(c/1000)}k</text>`}
 for(let i=0;i<=5;i++){const t=ym*i/5;s+=`<line x1="${m.l}" x2="${W-m.r}" y1="${Y(t)}" y2="${Y(t)}" stroke="#eef0f5"/><text x="${m.l-6}" y="${Y(t)+3}" font-size="10" text-anchor="end" fill="#889">${Math.round(t)}</text>`}
 s+=`<text x="${W/2}" y="${H-4}" font-size="11" text-anchor="middle" fill="#556">硬件成本 (USD)</text><text x="12" y="${H/2}" font-size="11" fill="#556" transform="rotate(-90 12 ${H/2})" text-anchor="middle">tok/s</text>`;
 s+=P.map(p=>`<circle class="dot" data-id="${p.id}" cx="${X(p.hardware_cost_usd)}" cy="${Y(p.tok_s)}" r="5" fill="${COL[p.source_level]}" fill-opacity=".7"><title>${esc(p.model)} · ${esc(p.hardware)} · ${p.tok_s} tok/s · $${p.hardware_cost_usd}</title></circle>`).join('');
 s+=Object.entries(COL).map(([k,c],i)=>`<circle cx="${W-180+i*44}" cy="16" r="5" fill="${c}"/><text x="${W-172+i*44}" y="20" font-size="11" fill="#556">${k}</text>`).join('');
 $('chart').innerHTML=s+(P.length?'':`<text x="320" y="150" text-anchor="middle" fill="#99a">当前筛选无可绘制数据</text>`);
 document.querySelectorAll('.dot').forEach(d=>d.onclick=()=>open(d.dataset.id));}
function open(id){const r=D.find(x=>x.id==id);$('dc').innerHTML=`<h2 style="margin-top:0">${esc(r.model)}</h2><p><span class="tag">${CAT[r.category]}</span> <span class="lv ${r.source_level}">${r.source_level}</span> <span class="tag">${r.id}</span></p>
<dl><dt>量化/优化</dt><dd>${v(r.quant)}</dd><dt>引擎</dt><dd>${esc(r.engine)}</dd><dt>硬件</dt><dd>${esc(r.hardware)}（${r.hardware_family}）</dd><dt>性能</dt><dd>${v(r.metric)}</dd><dt>单流 tok/s</dt><dd>${v(r.tok_s)}</dd><dt>并发</dt><dd>${v(r.concurrency)}</dd><dt>上下文</dt><dd>${v(r.context)}</dd><dt>硬件成本</dt><dd>${v(r.hardware_cost_text)}</dd><dt>$/tok/s</dt><dd>${v(r.cpt)}</dd><dt>日期</dt><dd>${v(r.date)}</dd><dt>来源说明</dt><dd>${v(r.source_note)}</dd></dl>
<h3>启动命令</h3>${r.launch_command?`<pre>${esc(r.launch_command)}</pre>`:`<pre># 未见公开数据\n# 你跑过这个配置？欢迎提交 PR 补全启动命令</pre>`}
<h3>来源</h3><p><a href="${esc(r.source_url)}" target="_blank" rel="noopener">${esc(r.source_url)}</a></p><p><a href="submit.html">✎ 提交修正 / 补充</a></p>`;
 $('drawer').classList.add('open');$('mask').classList.add('open');}
$('x').onclick=$('mask').onclick=()=>{$('drawer').classList.remove('open');$('mask').classList.remove('open')};
// deep-link: explore.html?max=3000&fam=Mac&q=...
const U=new URLSearchParams(location.search);
setTimeout(()=>{if(U.get('max'))$('budget').value=U.get('max');if(U.get('fam'))$('fam').value=U.get('fam');if(U.get('q'))$('q').value=U.get('q');if(U.get('id'))open(U.get('id'));render()},300);
