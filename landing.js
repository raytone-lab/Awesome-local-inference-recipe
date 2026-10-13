fetch('data/recipes.json').then(r=>r.json()).then(D=>{
const e=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const hot=D.filter(r=>r.x_post).sort((a,b)=>(b.x_post.likes+3*b.x_post.reposts)-(a.x_post.likes+3*a.x_post.reposts)).slice(0,9);
document.getElementById('hot').innerHTML=hot.map(r=>`<a class="hc" href="${e(r.source_url)}" target="_blank" rel="noopener">
<div class="hm"><span class="lv ${r.source_level}">${r.source_level}</span><span>♥ ${r.x_post.likes} · ⟲ ${r.x_post.reposts}</span></div>
<div class="big">${r.tok_s!=null?r.tok_s+'<small> tok/s</small>':'🎬'}</div><b>${e(r.model)}</b>
<div class="sub">${e(r.engine)} · ${e(r.quant||'')}</div><div class="sub">${e(r.hardware)}</div>
<div class="mt">${e(r.metric)}</div><div class="au">@${e(r.x_post.author)} · ${r.date}</div></a>`).join('');
const n=(f)=>D.filter(f).length;
document.getElementById('ks').innerHTML=[[D.length,'条配方'],[new Set(D.map(r=>r.engine.split(/[ （]/)[0])).size,'种引擎'],[new Set(D.map(r=>r.hardware_family)).size,'类硬件'],[Math.round(100*n(r=>r.source_url)/D.length)+'%','带来源链接'],[n(r=>r.source_level=='实测'),'条实测']].map(([a,b])=>`<div class="k"><b>${a}</b>${b}</div>`).join('');
});
