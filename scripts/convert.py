# One-off converter from /workspace/lir/rows.py. Never invents values: unparseable -> null.
import sys, re, json
sys.path.insert(0, '/workspace/lir'); import rows
NA = rows.NA
def nz(v): return None if (v is None or v.strip() in (NA, '') or v.startswith('未核实')) else v
ENG = [('strata','Strata'),('omlx','oMLX'),('dflash','DFlash'),('mlx','MLX'),('vllm','vLLM'),('sglang','SGLang'),('llama.cpp','llama.cpp'),('ik_llama','ik_llama.cpp'),('ollama','Ollama'),('lm studio','LM Studio'),('exllama','ExLlama'),('comfy','ComfyUI'),('draw things','Draw Things'),('tensorfold','TensorFold'),('trt','TensorRT'),('ktransformers','KTransformers'),('diffusers','Diffusers')]
def engine(s):
    l=s.lower()
    for k,v in ENG:
        if k in l: return v
    return '其他/未注明'
def hwfam(h):
    l=h.lower()
    if any(k in l for k in ['cmp','v100','p40','mi50','mi60','a100','p100','t4','a16','sxm','instinct']): return '二手数据中心卡'
    if any(k in l for k in ['mac','m3','m4','m5','m2 ultra','apple']): return 'Mac'
    if 'spark' in l or 'gb10' in l: return 'DGX Spark'
    if any(k in l for k in ['amd','rx ','radeon','strix','r9700','7900','ryzen ai','halo']): return 'AMD'
    if any(k in l for k in ['rtx','nvidia','4090','3090','5090','5070','5080','4060']): return 'NVIDIA 消费级'
    return '其他'
def cost(c):
    # only when exactly one $ figure, no per-card ambiguity
    if not c or '/张' in c or '超' in c: return None
    nums=re.findall(r'\$\s?([\d,]+(?:\.\d+)?)(k)?', c)
    if not nums: return None
    n,k=nums[0]; v=float(n.replace(',',''))*(1000 if k else 1)
    return round(v)
def tps(s):
    m=re.search(r'([\d.]+)\s*(?:[–-]\s*[\d.]+\s*)?tok/s', s)
    return float(m.group(1)) if m else None
LV={'官方':'官方','官方(项目方)':'官方','社区实测':'实测','社区转述':'转述','媒体实测':'实测'}
def lvl(t):
    for k,v in LV.items():
        if t.startswith(k): return v
    return '宣称' if ('预测' in t or '宣称' in t) else t
def date(url,label):
    m=re.search(r'(20\d\d-\d\d-\d\d)', label); return m.group(1) if m else None
out=[]
for cat,lst in [('text',rows.TEXT),('image',rows.IMAGE),('video-audio',rows.VIDEO)]:
    for i,r in enumerate(lst):
        model,quant,hw,speed,conc,ctx,c,url,src,tag=r
        out.append(dict(id=f'{cat}-{i+1:03d}',category=cat,model=model,quant=nz(quant),engine=engine(quant+' '+hw),
          hardware=hw,hardware_family=hwfam(hw),hardware_cost_text=nz(c),hardware_cost_usd=cost(nz(c)),
          metric=nz(speed),tok_s=tps(speed) if cat=='text' and nz(speed) else None,concurrency=nz(conc),context=nz(ctx),
          launch_command=None,source_url=url,source_note=src,source_level=lvl(tag),date=date(url,src)))
json.dump(out,open('data/recipes.json','w'),ensure_ascii=False,indent=1)
json.dump([dict(item=p[0],price=p[1],date=p[2],source=p[3]) for p in rows.PRICES],open('data/prices.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(out),Counter(o['source_level'] for o in out),Counter(o['hardware_family'] for o in out),Counter(o['engine'] for o in out),sum(o['tok_s'] is not None for o in out),sum(o['hardware_cost_usd'] is not None for o in out))
