// Usage: node scripts/validate.mjs  — minimal validator against schema/recipe.schema.json (no deps)
import fs from 'fs';
const S=JSON.parse(fs.readFileSync(new URL('../schema/recipe.schema.json',import.meta.url)));
const D=JSON.parse(fs.readFileSync(new URL('../data/recipes.json',import.meta.url)));
let err=0;const ids=new Set();
const typeOk=(v,t)=>[].concat(t).some(x=>x==='null'?v===null:x==='number'?typeof v==='number':typeof v===x);
for(const r of D){
  const e=m=>{err++;console.error(`[${r.id}] ${m}`)};
  if(ids.has(r.id))e('duplicate id');ids.add(r.id);
  for(const k of S.required) if(r[k]==null||r[k]==='')e(`missing ${k}`);
  for(const k of Object.keys(r)){const p=S.properties[k];if(!p){e(`unknown field ${k}`);continue}
    if(p.enum&&!p.enum.includes(r[k]))e(`${k} not in enum: ${r[k]}`);
    if(p.type&&!typeOk(r[k],p.type))e(`${k} wrong type`);
    if(p.pattern&&typeof r[k]==='string'&&!new RegExp(p.pattern).test(r[k]))e(`${k} pattern`);}
  if(r.hardware_cost_usd!=null&&r.hardware_cost_usd>30000)console.warn(`[${r.id}] warn: cost > $30k`);
}
console.log(err?`✗ ${err} errors`:`✓ ${D.length} recipes valid`);process.exit(err?1:0);
