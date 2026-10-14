// Usage: node scripts/check_dupes.mjs — fails on duplicate ids, exact duplicate rows, inconsistent source_id, dangling superseded_by.
import fs from 'fs';
import crypto from 'crypto';
const D=JSON.parse(fs.readFileSync(new URL('../data/recipes.json',import.meta.url)));
let err=0;const e=m=>{err++;console.error(m)};
const ids=new Map(),rows=new Map(),bySrc=new Map();
const norm=u=>{u=u.trim().split('#')[0].replace(/\/+$/,'').replace(/^http:\/\//,'https://').replace(/^https:\/\/(www\.)?(twitter|x)\.com\//i,'https://x.com/');return u.includes('x.com/')?u.replace(/\?.*$/,''):u};
for(const r of D){
  if(ids.has(r.id))e(`duplicate id ${r.id}`);ids.set(r.id,r);
  const key=JSON.stringify([norm(r.source_url),r.model,r.hardware,r.engine,r.quant??null,r.metric??null]);
  if(rows.has(key))e(`exact duplicate row: ${rows.get(key)} == ${r.id}`);else rows.set(key,r.id);
  const want='src-'+crypto.createHash('sha1').update(norm(r.source_url)).digest('hex').slice(0,10);
  if(r.source_id!==undefined&&r.source_id!==want)e(`[${r.id}] source_id ${r.source_id} != ${want} (run scripts/link_sources.py)`);
  (bySrc.get(norm(r.source_url))||bySrc.set(norm(r.source_url),[]).get(norm(r.source_url))).push(r.id);
}
for(const r of D)if(r.superseded_by!=null&&!ids.has(r.superseded_by))e(`[${r.id}] superseded_by unknown id ${r.superseded_by}`);
const shared=[...bySrc.values()].filter(v=>v.length>1);
console.log(err?`✗ ${err} duplicate/link errors`:`✓ no duplicates · ${bySrc.size} sources · ${shared.length} shared by multiple rows`);
process.exit(err?1:0);
