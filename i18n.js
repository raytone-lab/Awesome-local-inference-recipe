// Shared zh/en switch. Priority: ?lang= (persisted) > localStorage > browser language. Pages call T(key); static nodes use data-i18n (HTML) / data-i18n-ph (placeholder).
(function(){
const P=new URLSearchParams(location.search),norm=l=>(l||'').toLowerCase().startsWith('zh')?'zh-CN':(l?'en':'');
let L=norm(P.get('lang'));
try{if(L)localStorage.setItem('lang',L);else L=norm(localStorage.getItem('lang'))}catch(e){}
if(!L)L=((navigator.languages&&navigator.languages[0])||navigator.language||'').toLowerCase().startsWith('zh')?'zh-CN':'en';
window.LANG=L;document.documentElement.lang=L;
const S={
 'zh-CN':{home:'首页',explore:'配方库',speed:'速度体感',submit:'提交配方',brand:'本地推理配方',
  lvl:{'官方':'官方','实测':'实测','转述':'转述','宣称':'宣称'},fam:{},cat:{text:'文字',image:'图像','video-audio':'影音'},
  na:'未见公开数据'},
 en:{home:'Home',explore:'Explore',speed:'Speed feel',submit:'Submit',brand:'Local Inference Recipes',
  lvl:{'官方':'Official','实测':'Measured','转述':'Relayed','宣称':'Claimed'},
  fam:{'Mac':'Mac','NVIDIA 消费级':'NVIDIA consumer','DGX Spark':'DGX Spark','AMD':'AMD','二手数据中心卡':'Used datacenter','其他':'Other'},
  cat:{text:'Text',image:'Image','video-audio':'Video & audio'},na:'no public data'}};
window.I18N_ADD=(d)=>{for(const k in d)Object.assign(S[k],d[k])};
window.T=(k,o)=>{let s=S[L][k];if(s==null)s=S['zh-CN'][k];if(s==null)return k;if(o)for(const a in o)s=s.split('{'+a+'}').join(o[a]);return s};
window.TL=v=>S[L].lvl[v]||v;window.TF=v=>S[L].fam[v]||v;window.TC=v=>S[L].cat[v]||v;
window.setLang=l=>{try{localStorage.setItem('lang',l)}catch(e){}const p=new URLSearchParams(location.search);p.delete('lang');location.href=location.pathname+(p.toString()?'?'+p:'')+location.hash};
window.applyI18n=()=>{
 document.querySelectorAll('[data-i18n]').forEach(e=>e.innerHTML=T(e.dataset.i18n));
 document.querySelectorAll('[data-i18n-ph]').forEach(e=>e.placeholder=T(e.dataset.i18nPh));
 const n=document.querySelector('header nav');
 if(n&&!n.querySelector('.lang')){const s=document.createElement('span');s.className='lang';
  s.innerHTML=`<a href="#" data-l="en">EN</a><a href="#" data-l="zh-CN">中文</a>`;n.appendChild(s);}
 if(n)n.querySelectorAll('.lang [data-l]').forEach(a=>{a.classList.toggle('on',a.dataset.l===L);a.onclick=e=>{e.preventDefault();setLang(a.dataset.l)}});
 if(S[L].title)document.title=S[L].title;
 document.documentElement.classList.toggle('l-en',L==='en');};
})();
