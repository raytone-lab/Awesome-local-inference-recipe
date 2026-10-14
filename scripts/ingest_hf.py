#!/usr/bin/env python3
"""Hugging Face 模型卡 -> 候选配方（不会写入 data/recipes.json）。
用法: python3 scripts/ingest_hf.py [--limit 40] [--libs gguf,mlx] [--sorts trendingScore,downloads]
可选环境变量 HF_TOKEN。仅用标准库。"""
import argparse  # v2: 抽取逻辑见 scripts/hf_extract.py
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from normalize_engines import canon  # 统一引擎名
import argparse, datetime, glob, json, os, re, sys, time, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://huggingface.co/api/models"
UA = "awesome-local-inference-recipes-ingest/0.1 (+local research)"
SPEED = re.compile(r"(\d+(?:\.\d+)?)\s*\**\s*(tok/s|tokens?/s(?:ec)?|t/s|tps)\b", re.I)
PREFILL = re.compile(r"prompt|prefill|pp\d*|read|ingest|处理|读入", re.I)
GEN = re.compile(r"decode|generat|tg\d*|output|eval|生成", re.I)
QUANT = re.compile(r"\b(?:UD-)?(?:I?Q\d(?:_[0-9A-Z]+)*|MXFP4|NVFP4|FP8|BF16|F16|\d-?bit|AWQ|GPTQ|EXL[23])\b", re.I)
HW = re.compile(r"\b(RTX\s?\d{4}(?:\s?Ti)?|[3-5]090|4080|V100|P40|MI50|MI60|A6000|7900\s?XTX|Strix Halo|DGX Spark|Spark|M[1-5]\s?(?:Pro|Max|Ultra)?|Mac\s?(?:Studio|mini|Book Pro)|\d+\s?GB\s?(?:VRAM|RAM|unified))\b", re.I)
ENG = re.compile(r"\b(llama\.cpp|llama-server|llama-bench|vLLM|SGLang|MLX|mlx-lm|oMLX|Ollama|LM Studio|Strata|ExLlamaV[23]|TensorRT|ik_llama|KTransformers|DFlash2?|MTP)\b", re.I)
CTX = re.compile(r"(\d+(?:\.\d+)?)\s*[Kk]\s*(?:context|ctx|tokens)|context(?: length| window)?[^\n\d]{0,20}(\d[\d,]*\s*[Kk]?)", re.I)

def get(url, token, as_json=True, tries=3):
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Authorization": f"Bearer {token}"} if token else {})})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                b = r.read().decode("utf-8", "replace")
                return json.loads(b) if as_json else b
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code == 429: time.sleep(10 * (i + 1)); continue
            return None
        except Exception:
            time.sleep(3)
    return None

def noise(mid):
    name = mid.split("/")[-1]
    parts = re.split(r"[-_.]", name)
    brands = sum(bool(re.match(r"(?i)(opus|gpt|grok|claude|gemini|dsv|deepseek|kimi|k\d|qwen|glm|sonnet)", p)) for p in parts)
    if len(name) > 70 or brands >= 4: return "id 堆砌多个模型名（疑似 merge/刷榜）"
    if re.search(r"(?i)uncensored|abliterat|nsfw|roleplay|humanizer", name): return "非性能向变体（uncensored/角色扮演等）"
    return None

def uniq(rx, text, n=6):
    out = []
    for m in rx.finditer(text):
        v = re.sub(r"\s+", " ", m.group(0)).strip()
        if v.lower() not in [o.lower() for o in out]: out.append(v)
    return out[:n]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--libs", default="gguf,mlx")
    ap.add_argument("--sorts", default="trendingScore,downloads")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--ids", help="逗号分隔的 repo id，只抓这些（重测用，不按历史去重）")
    ap.add_argument("--include-nonconsumer", action="store_true", help="保留机房/工作站卡行")
    ap.add_argument("--out", help="输出文件（默认 data/candidates/hf-YYYY-MM-DD.json）")
    a = ap.parse_args()
    tok = os.environ.get("HF_TOKEN")
    seen_urls = {r.get("source_url") for r in json.load(open(f"{ROOT}/data/recipes.json"))}
    seen_fp = {}; seen_rows = set()
    for f in glob.glob(f"{ROOT}/data/candidates/*.json"):
        if a.out and os.path.abspath(f) == os.path.abspath(a.out): continue
        try:
            for c in json.load(open(f))["candidates"]:
                seen_urls.add(c["model_url"])
                if c.get("table_fingerprint"): seen_fp[c["table_fingerprint"]] = c["id"]
                for r in c.get("rows", []):
                    if r.get("dup_key"): seen_rows.add(r["dup_key"])
        except Exception: pass
    models = {}
    if a.ids:
        for mid in a.ids.split(","):
            models[mid] = get(f"{API}/{mid}", tok) or {"id": mid}; time.sleep(a.delay)
    for lib in ([] if a.ids else a.libs.split(",")):
        for s in a.sorts.split(","):
            q = urllib.parse.urlencode({"filter": lib, "sort": s, "direction": -1, "limit": a.limit})
            for m in get(f"{API}?{q}", tok) or []:
                models.setdefault(m["id"], m)
            time.sleep(a.delay)
    from hf_extract import extract
    cands, filtered = [], {"dup": 0, "dup_table": [], "noise": [], "no_speed": 0, "no_card": 0, "only_nonconsumer": []}
    for mid, m in models.items():
        url = f"https://huggingface.co/{mid}"
        if url in seen_urls and not a.ids: filtered["dup"] += 1; continue
        why = noise(mid)
        if why: filtered["noise"].append({"id": mid, "reason": why}); continue
        card = get(f"{url}/raw/main/README.md", tok, as_json=False); time.sleep(a.delay)
        if not card: filtered["no_card"] += 1; continue
        x = extract(mid, card, include_nonconsumer=a.include_nonconsumer, seen_rows=seen_rows)
        if not x["rows"]: filtered["no_speed"] += 1; continue
        if any("非通用" in f for f in x["flags"]): filtered["noise"].append({"id": mid, "reason": x["flags"][0]}); continue
        if not x["primary"]:
            if all(r.get("duplicate") for r in x["rows"] if r["gen"] is not None): filtered["dup_table"].append({"id": mid, "same_as": "行级重复"}); continue
            filtered["only_nonconsumer"].append(mid); continue
        fp = x["table_fingerprint"]
        if fp in seen_fp:
            filtered["dup_table"].append({"id": mid, "same_as": seen_fp[fp]}); continue
        seen_fp[fp] = mid
        p = x["primary"]; kept = [r for r in x["rows"] if not r["excluded"]]
        need = [k for k, v in {"hardware": p["hardware"], "quant": p["quant"], "context": x["context_tokens"]}.items() if not v]
        need += ["engine 版本", "launch_command", "concurrency", "hardware_cost_usd"]
        name = mid.split("/")[-1]
        cands.append({
            "id": f"hf-{mid.replace('/', '--')}", "category": "text", "model": re.sub(r"(?i)[-_](gguf|mlx.*)$", "", name),
            "quant": p["quant"], "engine": ", ".join(uniq(ENG, card)) or None, "engine_canonical": canon(", ".join(uniq(ENG, card))) if uniq(ENG, card) else "Unspecified", "hardware": p["hardware"],
            "metric": f"生成 {p['gen']} tok/s" + (f"；读入 {p['prefill']} tok/s" if p["prefill"] else ""),
            "tok_s": p["gen"], "context_tokens": p.get("context_tokens") or x["context_tokens"], "source_url": url, "source_level": p.get("level", "宣称"),
            "concurrency": (f"聚合 {p['aggregate']} tok/s" if p.get("aggregate") else None), "peak_claim": p.get("peak_claim"),
            "date": (m.get("createdAt") or "")[:10] or None, "model_url": url, "downloads": m.get("downloads"), "likes": m.get("likes"),
            "rows": kept, "excluded_rows": [r for r in x["rows"] if r["excluded"]], "caveats": x["caveats"], "flags": x["flags"],
            "table_fingerprint": fp, "raw_snippet": [r["raw"] for r in kept][:12],
            "extracted_confidence": x["confidence"], "needs_review": need, "extractor": "v2"})
    cands.sort(key=lambda c: (-c["extracted_confidence"], -(c["downloads"] or 0)))
    today = datetime.date.today().isoformat()
    out = a.out or f"{ROOT}/data/candidates/hf-{today}.json"
    json.dump({"generated": datetime.datetime.now().astimezone().isoformat(), "scanned": len(models), "filtered": filtered, "candidates": cands},
              open(out, "w"), ensure_ascii=False, indent=1)
    print(f"扫描 {len(models)} 个模型 | 候选 {len(cands)} | 去重 {filtered['dup']}+同表 {len(filtered['dup_table'])} | 仅机房/工作站 {len(filtered['only_nonconsumer'])} | 噪声 {len(filtered['noise'])} | 无测速 {filtered['no_speed']} | 无模型卡 {filtered['no_card']}\n-> {out}")

if __name__ == "__main__": main()
