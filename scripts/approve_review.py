#!/usr/bin/env python3
"""把 review.json 中 decision=收录 的条目写入 data/recipes.json（幂等）。用法: python3 scripts/approve_review.py data/candidates/hf-2026-10-13.review.json"""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COST = {"RTX 5090 32GB": ("仅显卡 $5,400 起（2026-10-11 最低追踪报价，见 prices.json）", 5400),
        "RTX 4090 24GB": ("仅显卡 二手约 $2,214（2026-10-06 eBay 成交，见 prices.json）", 2214)}
def fam(hw):
    if re.search(r"Mac|iPhone", hw): return "Mac" if "Mac" in hw else "其他"
    if re.search(r"RTX PRO", hw): return "其他"
    return "NVIDIA 消费级"
rp = sys.argv[1]; rev = json.load(open(rp))
recipes = json.load(open(f"{ROOT}/data/recipes.json")); ids = {r["id"] for r in recipes}
cand_file = rp.replace(".review.json", ".json"); cand = json.load(open(cand_file))
MODEL = {"hf-prism-ml--Ternary-Bonsai-2-27B-gguf": "Ternary Bonsai 2 27B", "hf-prism-ml--Bonsai-27B-mlx-1bit": "Bonsai 27B 1-bit",
         "hf-cdiamond--Qwen3.8-27B-iMatrix-NVFP4-MTP-GGUF": "Qwen3.8-27B"}
NOTE = {"hf-prism-ml--Ternary-Bonsai-2-27B-gguf": "需 PrismML llama.cpp fork（原版 llama.cpp 不可用）",
        "hf-prism-ml--Bonsai-27B-mlx-1bit": "需 PrismML llama.cpp / mlx-swift fork",
        "hf-cdiamond--Qwen3.8-27B-iMatrix-NVFP4-MTP-GGUF": "RTX PRO 4000 Blackwell SFF 为工作站卡，价格未找到可靠来源；博客 https://piszczek.pl/blog/qwen38-27b-256k-50-tps-24gb-gpu"}
added = 0
for x in rev["reviews"]:
    if x["decision"] != "收录": continue
    slug = re.sub(r"[^a-z0-9]+", "-", x["id"][3:].lower()).strip("-")
    for i, y in enumerate(x["recipes"], 1):
        rid = f"hf-{slug}-{i}"
        if rid in ids: continue
        hw = y["hardware"]; ct, cu = COST.get(hw, (None, None))
        notes = "; ".join(filter(None, ["HF 模型卡（作者自报）", NOTE[x["id"]], y.get("note"), "原文: " + y["quote"]]))
        metric = f"{y['gen_tok_s']} tok/s 生成" + (f"；{y['prefill_tok_s']} tok/s 读入" if y["prefill_tok_s"] else "")
        recipes.append({"id": rid, "category": "text", "model": MODEL[x["id"]], "quant": y["quant"], "engine": y["engine"],
            "hardware": hw, "hardware_family": fam(hw), "hardware_cost_text": ct, "hardware_cost_usd": cu,
            "metric": metric, "tok_s": y["gen_tok_s"], "concurrency": x.get("concurrency"), "context": x.get("context"),
            "launch_command": x.get("launch_command") if "cdiamond" in x["id"] else x.get("launch_command"),
            "source_url": x["url"], "source_note": notes, "source_level": x.get("source_level", "宣称"),
            "date": x["card_date"][:10],
            "metric_en": f"{y['gen_tok_s']} tok/s decode" + (f"; {y['prefill_tok_s']} tok/s prefill" if y["prefill_tok_s"] else "")})
        added += 1
    for c in cand["candidates"]:
        if c["id"] == x["id"]: c["status"] = "approved"
for x in rev["reviews"]:
    for c in cand["candidates"]:
        if c["id"] == x["id"] and x["decision"] == "拒绝": c["status"] = "rejected"; c["reject_reason"] = x["reason"]
json.dump(recipes, open(f"{ROOT}/data/recipes.json", "w"), ensure_ascii=False, indent=2)
json.dump(cand, open(cand_file, "w"), ensure_ascii=False, indent=1)
print(f"新增 {added}，总计 {len(recipes)}")
