#!/usr/bin/env python3
"""Hugging Face 模型卡 -> 候选配方（不会写入 data/recipes.json）。
用法: python3 scripts/ingest_hf.py [--limit 40] [--libs gguf,mlx] [--sorts trendingScore,downloads]
可选环境变量 HF_TOKEN。仅用标准库。"""
import argparse, datetime, glob, json, os, re, sys, time, urllib.request, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://huggingface.co/api/models"
UA = "RecipeBench-ingest/0.1 (+local research)"
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

def extract(text):
    gen, pre, snippets = [], [], []
    for line in text.splitlines():
        if not SPEED.search(line): continue
        s = line.strip()[:300]
        nums = [float(m.group(1)) for m in SPEED.finditer(line)]
        if s.startswith("|") and not nums: continue
        (pre if PREFILL.search(line) and not GEN.search(line) else gen).extend(nums)
        snippets.append(s)
    # 表格: 表头里有 t/s 列
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.strip().startswith("|") and re.search(r"t/s|tok/s|tokens/s", l, re.I):
            hdr = [c.strip() for c in l.strip().strip("|").split("|")]
            for row in lines[i + 2:i + 30]:
                if not row.strip().startswith("|"): break
                cells = [c.strip(" *`") for c in row.strip().strip("|").split("|")]
                snippets.append(row.strip()[:300])
                for h, c in zip(hdr, cells):
                    m = re.match(r"^(\d+(?:\.\d+)?)$", c.replace(",", ""))
                    if m and re.search(r"t/s|tok|tps", h, re.I):
                        (pre if PREFILL.search(h) else gen).append(float(m.group(1)))
    return gen, pre, list(dict.fromkeys(snippets))[:12]

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
    a = ap.parse_args()
    tok = os.environ.get("HF_TOKEN")
    seen_urls = {r.get("source_url") for r in json.load(open(f"{ROOT}/data/recipes.json"))}
    for f in glob.glob(f"{ROOT}/data/candidates/*.json"):
        try: seen_urls |= {c["model_url"] for c in json.load(open(f))["candidates"]}
        except Exception: pass
    models = {}
    for lib in a.libs.split(","):
        for s in a.sorts.split(","):
            q = urllib.parse.urlencode({"filter": lib, "sort": s, "direction": -1, "limit": a.limit})
            for m in get(f"{API}?{q}", tok) or []:
                models.setdefault(m["id"], m)
            time.sleep(a.delay)
    cands, filtered = [], {"dup": 0, "noise": [], "no_speed": 0, "no_card": 0}
    for mid, m in models.items():
        url = f"https://huggingface.co/{mid}"
        if url in seen_urls: filtered["dup"] += 1; continue
        why = noise(mid)
        if why: filtered["noise"].append({"id": mid, "reason": why}); continue
        card = get(f"{url}/raw/main/README.md", tok, as_json=False); time.sleep(a.delay)
        if not card: filtered["no_card"] += 1; continue
        gen, pre, snip = extract(card)
        if not gen and not pre: filtered["no_speed"] += 1; continue
        hw, eng, qu = uniq(HW, card), uniq(ENG, card), uniq(QUANT, card)
        ctx = [c for c in uniq(CTX, card, 3)]
        need = [k for k, v in {"hardware": hw, "engine": eng, "context": ctx, "launch_command": None, "concurrency": None, "hardware_cost_usd": None}.items() if not v]
        if not gen: need.append("generation_tok_s")
        conf = round(min(1.0, 0.3 + 0.2 * bool(gen) + 0.2 * bool(hw) + 0.15 * bool(eng) + 0.15 * bool(qu)), 2)
        name = mid.split("/")[-1]
        cands.append({
            "id": f"hf-{mid.replace('/', '--')}", "category": "text" if "text" in (m.get("pipeline_tag") or "text") else m.get("pipeline_tag"),
            "model": re.sub(r"(?i)[-_](gguf|mlx.*)$", "", name), "quant": ", ".join(qu) or None,
            "engine": ", ".join(eng) or None, "hardware": ", ".join(hw) or None, "hardware_family": None,
            "hardware_cost_text": None, "hardware_cost_usd": None,
            "metric": "; ".join(filter(None, [gen and f"生成 {max(gen)} tok/s (卡内最大值)", pre and f"读入 {max(pre)} tok/s"])),
            "tok_s": max(gen) if gen else None, "gen_tok_s_all": gen[:20], "prefill_tok_s_all": pre[:20],
            "concurrency": None, "context": ", ".join(ctx) or None, "launch_command": None,
            "source_url": url, "source_note": "HF 模型卡（作者自报）", "source_level": "宣称",
            "date": (m.get("createdAt") or "")[:10] or None,
            "model_url": url, "downloads": m.get("downloads"), "likes": m.get("likes"), "pipeline_tag": m.get("pipeline_tag"),
            "raw_snippet": snip, "extracted_confidence": conf, "needs_review": need})
    cands.sort(key=lambda c: (-c["extracted_confidence"], -(c["downloads"] or 0)))
    today = datetime.date.today().isoformat()
    out = f"{ROOT}/data/candidates/hf-{today}.json"
    json.dump({"generated": datetime.datetime.now().astimezone().isoformat(), "scanned": len(models), "filtered": filtered, "candidates": cands},
              open(out, "w"), ensure_ascii=False, indent=1)
    print(f"扫描 {len(models)} 个模型 | 候选 {len(cands)} | 去重 {filtered['dup']} | 噪声 {len(filtered['noise'])} | 无测速 {filtered['no_speed']} | 无模型卡 {filtered['no_card']}\n-> {out}")

if __name__ == "__main__": main()
