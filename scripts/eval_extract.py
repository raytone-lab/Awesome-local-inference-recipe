#!/usr/bin/env python3
"""用审查文件当金标准评估抽取器。
python3 scripts/eval_extract.py <review.json> [--old candidates.json]
指标：主值命中（主值 ∈ 金标准生成值）、行召回（金标准生成值被抽到）、拒绝卡信号（标记/同表/无主值）。"""
import json, os, sys, argparse
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{R}/scripts")
from hf_extract import extract
ap = argparse.ArgumentParser(); ap.add_argument("reviews", nargs="+"); ap.add_argument("--old", nargs="*", default=[]); ap.add_argument("-v", action="store_true"); a = ap.parse_args()
fps = {}; seen = set()
for ri, rf in enumerate(a.reviews):
  rev = json.load(open(rf))["reviews"]
  old = {c["id"]: c for c in json.load(open(a.old[ri]))["candidates"]} if ri < len(a.old) else {}
  t = dict(cards=0, old_p=0, new_p=0, gold=0, hit=0, rej=0, rej_sig=0)
  def close_(x, s): return x is not None and any(g is not None and abs(x - g) < 1e-6 for g in s)
  for x in rev:
      mid = x["id"][3:].replace("--", "/", 1)
      text = open(f"{R}/tests/fixtures/hf/{mid.replace('/', '_', 1)}.md").read()
      e = extract(mid, text, include_nonconsumer=True, seen_rows=seen); e0 = extract(mid, text, include_nonconsumer=True)
      g = [y["gen_tok_s"] for y in x["recipes"]]
      if x["decision"] == "拒绝":
          t["rej"] += 1
          dup = e["table_fingerprint"] in fps or any(r.get("dup_key") in fps for r in e["rows"])
          sig = bool(e["flags"]) or not e["primary"] or dup or (e["primary"] or {}).get("hw_class") in ("datacenter","workstation") or all(r["duplicate"] for r in e["rows"] if r["gen"] is not None)
          t["rej_sig"] += sig
          if a.v: print(f"REJ {mid:60} signal={sig} flags={e['flags']}")
      elif g:
          t["cards"] += 1
          t["old_p"] += close_((old.get(x["id"]) or {}).get("tok_s"), g)
          pp = e["primary"] or e0["primary"]; p = pp["gen"] if pp else None
          t["new_p"] += close_(p, g)
          got = [r["gen"] for r in e["rows"]]
          h = sum(close_(v, got) for v in g); t["gold"] += len(g); t["hit"] += h
          if a.v: print(f"{'OK ' if close_(p, g) and h == len(g) else 'XX '}{mid:60} primary={p} gold={g} recall={h}/{len(g)} hw={e0['primary']['hardware'] if e0['primary'] else None}")
      fps[e["table_fingerprint"]] = mid
      for r in e["rows"]: fps[r.get("dup_key")] = mid
  print(f"[{os.path.basename(rf)}] 有效卡 {t['cards']}：主值命中 旧 {t['old_p']}/{t['cards']} → 新 {t['new_p']}/{t['cards']}；行召回 {t['hit']}/{t['gold']}；拒绝卡有信号 {t['rej_sig']}/{t['rej']}")
