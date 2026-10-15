// Shared by the home page and the explorer: what a row's hardware_cost_usd actually prices, so $/tok/s is only ranked like-for-like.
// 'gpu' = card price only (cost text says 仅显卡, or a discrete-card family: NVIDIA consumer / AMD cards / used datacenter / named workstation cards);
// 'sys' = whole machine (Mac, DGX Spark, Strix Halo / Ryzen AI Max mini PCs, phones/tablets, rows priced as 整机);
// null = no price, or a comparison row ("A / B", "A vs B") whose single price can't be attributed.
(function(){
const DISCRETE=['NVIDIA 消费级','AMD','二手数据中心卡'],WHOLE=['Mac','DGX Spark'];
const SYS=/Strix Halo|Ryzen AI Max|Mac\b|Mac mini|iPhone|iPad|Samsung|AI TOP ATOM|GB10/i,CARD=/RTX|Radeon|\bRX\s*\d|R9700|Tesla|CMP|\bArc\b|\bMI\d{2,3}\b|V100|P40/i;
window.costKind=r=>{if(r.hardware_cost_usd==null)return null;const h=r.hardware||'',t=r.hardware_cost_text||'';
 if(/\s\/\s|\svs\s/i.test(h))return null;
 if(t.includes('仅显卡'))return 'gpu';
 if(WHOLE.includes(r.hardware_family)||t.includes('整机')||SYS.test(h))return 'sys';
 if(DISCRETE.includes(r.hardware_family)||CARD.test(h))return 'gpu';
 return 'sys'};
// Rows whose metric says 自称 ("self-reported") are filed as 实测 but have no log behind them; keep them out of "measured" rankings until the data is fixed.
window.selfReported=r=>/自称/.test(r.metric||'');
})();
