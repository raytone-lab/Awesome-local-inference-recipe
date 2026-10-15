// Shared header behaviour on every page: collapsible nav, theme toggle (persisted), labels for the header controls in en / zh-CN / ja.
(function(){
const L=(document.documentElement.lang||'en').toLowerCase(),K=L.startsWith('zh')?'zh':L.startsWith('ja')?'ja':'en';
const S={en:{star:'Star on GitHub',starS:'Star',menu:'Menu',dark:'Switch to dark mode',light:'Switch to light mode',skip:'Skip to content',nav:'Main',foot:'Footer'},
 zh:{star:'在 GitHub 上 Star',starS:'Star',menu:'菜单',dark:'切换到深色模式',light:'切换到浅色模式',skip:'跳到正文',nav:'主导航',foot:'页脚'},
 ja:{star:'GitHub でスター',starS:'Star',menu:'メニュー',dark:'ダークモードに切り替え',light:'ライトモードに切り替え',skip:'本文へスキップ',nav:'メイン',foot:'フッター'}}[K];
document.querySelectorAll('[data-s]').forEach(e=>e.textContent=S[e.dataset.s]);
document.querySelectorAll('.hd-star').forEach(e=>e.setAttribute('aria-label',S.star));
document.querySelectorAll('#nav').forEach(e=>e.setAttribute('aria-label',S.nav));document.querySelectorAll('.site-ft nav').forEach(e=>e.setAttribute('aria-label',S.foot));
const R=document.documentElement,mq=matchMedia('(prefers-color-scheme: dark)');
const cur=()=>R.getAttribute('data-theme')||(mq.matches?'dark':'light');
const tb=document.querySelector('.theme-tg');
const lab=()=>{if(!tb)return;const d=cur()==='dark';tb.setAttribute('aria-label',d?S.light:S.dark);tb.title=d?S.light:S.dark;tb.setAttribute('aria-pressed',String(d));};
if(tb){tb.onclick=()=>{const t=cur()==='dark'?'light':'dark';R.setAttribute('data-theme',t);try{localStorage.setItem('theme',t)}catch(e){}lab();document.dispatchEvent(new CustomEvent('themechange'))};lab();mq.addEventListener&&mq.addEventListener('change',lab);}
const nb=document.querySelector('.nav-tg'),nav=document.getElementById('nav');
if(nb&&nav){nb.setAttribute('aria-label',S.menu);
 const set=o=>{nb.setAttribute('aria-expanded',String(o));document.body.classList.toggle('nav-open',o)};
 nb.onclick=()=>set(nb.getAttribute('aria-expanded')!=='true');
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('nav-open')){set(false);nb.focus()}});
 nav.addEventListener('click',e=>{if(e.target.closest('a[href]'))set(false)});
 matchMedia('(min-width: 861px)').addEventListener('change',e=>{if(e.matches)set(false)});}
})();
