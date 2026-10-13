#!/usr/bin/env python3
"""对比 v1（旧候选文件）与 v2（hf_extract）在已审 10 张卡上的准确率。金标准 = review.json。"""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{R}/scripts")
from hf_extract import extract
rev = json.load(open(f"{R}/data/candidates/hf-2026-10-13.review.json"))["reviews"]
old = {c["id"]: c for c in json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/old-hf.json"))["candidates"]}
tot = dict(n=0, old_p=0, new_p=0, gold_rows=0, new_hit=0, new_rows=0, new_wrong=0, old_hw_wrong=0, new_hw_ok=0)
print(f"{'card':48} {'gold主值':>9} {'v1':>8} {'v2':>8}  行召回")
for x in rev:
    mid = x["id"][3:].replace("--", "/", 1)
    text = open(f"{R}/tests/fixtures/hf/{mid.replace('/', '_', 1)}.md").read()
    e = extract(mid, text, include_nonconsumer=True)
    gold = [(y["gen_tok_s"], y["prefill_tok_s"]) for y in x["recipes"]]
    gset = {g for g, _ in gold}
    o = old[x["id"]]["tok_s"]
    allowed = [r for r in e["rows"]]
    n_primary = e["primary"]["gen"] if e["primary"] else None
    if gold:
        tot["n"] += 1; tot["old_p"] += o in gset; tot["new_p"] += n_primary in gset
        got = {(r["gen"], r["prefill"]) for r in e["rows"]}
        hit = sum((g, p) in got or any(r["gen"] == g for r in e["rows"]) for g, p in gold)
        tot["gold_rows"] += len(gold); tot["new_hit"] += hit
    else:
        # 拒绝卡：v2 是否给出降级信号（标记/排除/同表）
        pass
    print(f"{mid:48} {str(gold[0][0]) if gold else x['decision']:>9} {str(o):>8} {str(n_primary):>8}  {hit if gold else '-'}/{len(gold)}  flags={e['flags']}")
print(tot)
