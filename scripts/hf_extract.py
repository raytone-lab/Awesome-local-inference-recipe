"""模型卡测速抽取（纯函数，便于测试）。v2 规则：
- 表格逐行解析：一行 = 硬件 × 量化/配置；按表头区分 生成(TG/decode/generation/tok/s) 与 读入(PP/prefill/prompt)
- 多量化表头（如 "PQ2_0 TG128 | PTQ1_0 TG128"）拆成多条
- 硬件只取自表格行标签或测速声明句（measured on / Hardware: / GPU0: / on one X）
- 机房/工作站卡打标签，默认排除（excluded=True）
- 保留说明（pending re-measurement 等）写入 caveats
- OCR / <3B / 占位链接 → 降可信度
- 上下文取数值（tokens）"""
import re, hashlib

DC = re.compile(r"\b(H100|H200|H20|B200|B300|GB200|A100|A800|L40S?|L4\b|A10G?|T4\b|MI300X?|MI325X?|Gaudi)", re.I)
WS = re.compile(r"\b(RTX\s?PRO\s?\d{4}|RTX\s?6000(?:\s?Ada)?|RTX\s?A\d{4}|A6000|RTX\s?[45]000\s?Ada)", re.I)
HW = re.compile(r"(RTX\s?PRO\s?\d{4}(?:\s?Blackwell)?(?:\s?SFF(?:\s?Edition)?)?|RTX\s?\d{4}(?:\s?Ti)?(?:\s?Ada)?(?:\s?\(\d+\s?GB\))?|\b[2-5]0[6-9]0(?:\s?Ti)?\b|\bV100\b|\bP40\b|\bMI50\b|\bMI60\b|7900\s?XTX|Strix Halo|DGX Spark|\bH100(?:\s?(?:SXM|NVL|PCIe))?|\bA100(?:\s?SXM)?|\bL40S?\b|\bL4\b|iPhone\s?\d+(?:\s?Pro(?:\s?Max)?)?|(?:Apple\s)?M[1-5]\s?(?:Pro|Max|Ultra)\b|Mac\s?(?:Studio|mini))", re.I)
QUANT = re.compile(r"\b(?:UD-)?(?:P?T?I?Q\d(?:_[0-9A-Z]+)*|MXFP4|NVFP4|FP8|BF16|F16|GPTQ-Int4|AWQ|EXL[23]|\d-bit)\b", re.I)
GEN_H = re.compile(r"\btg\d+\b|decode|generat|\beval\b|output|生成", re.I)
PRE_H = re.compile(r"\bpp\d+\b|prefill|prompt|读入|ingest", re.I)
SPEED_H = re.compile(r"t/s|tok/s|tokens?/s|\btps\b|\btg\d+\b|\bpp\d+\b", re.I)
NUM = re.compile(r"^\**~?\s*(\d[\d,]*(?:\.\d+)?)\s*\**\s*[¹²³*]*\s*(?:tok/s|t/s)?(?:\s*(?:mean|,).*)?$", re.I)
VAL_SPEED = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(?:tok/s|t/s|tokens?/s)", re.I)
DECL = re.compile(r"(measured (?:on|with)|hardware:|gpu0:|tested on|on (?:one|an?|my|our) |decode speed on|benchmarks? \()", re.I)
CAVEAT = re.compile(r"(pending re-?measurement|not a specification|thermally limited|separate measurements|not the same run|our numbers on our box|earlier .{0,20}build|estimates? rather than)", re.I)
CTX = re.compile(r"(?:ctx-size|context(?:\s+length|\s+window)?|上下文)[^\n\d]{0,30}?(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?\s?[KkM]\b|\d{4,7})|(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?\s?[KkM])[- ](?:token )?context", re.I)
PLACEHOLDER = re.compile(r"github\.com/your-org|github\.com/USERNAME|example\.com/", re.I)

def num(s):
    s = re.sub(r"[`*\[\]]", "", s).strip()
    m = NUM.match(s)
    return float(m.group(1).replace(",", "")) if m else None

def hw_class(hw):
    if not hw: return None
    if DC.search(hw): return "datacenter"
    if WS.search(hw): return "workstation"
    return "consumer"

def ctx_tokens(text):
    best = None
    for m in CTX.finditer(text):
        v = (m.group(1) or m.group(2) or "").replace(",", "").replace(" ", "")
        try:
            n = float(v[:-1]) * (1024 if v[-1] in "Kk" else 1024 ** 2) if v[-1] in "KkM" else float(v)
        except ValueError: continue
        n = int(n)
        if v[-1] in "Kk" and n % 1024 == 0 and int(v[:-1].split('.')[0]) in (128, 256, 262, 32, 64, 8, 4, 16, 1000): pass
        if 2048 <= n <= 10_000_000: best = max(best or 0, n)
    return best

def declared_hardware(text):
    hws = []
    for line in text.splitlines():
        if DECL.search(line):
            for m in HW.finditer(line):
                h = re.sub(r"\s+", " ", m.group(0)).strip()
                if h not in hws: hws.append(h)
    return hws

def split_row(l): return [c.strip() for c in l.strip().strip("|").split("|")]

def parse_tables(text):
    """返回行记录 list[dict(hardware, quant, label, gen, prefill, raw)]"""
    lines, out, i = text.splitlines(), [], 0
    while i < len(lines):
        l = lines[i]
        if l.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            hdr = split_row(l); rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"): rows.append(lines[j]); j += 1
            out += _table(hdr, rows); i = j; continue
        i += 1
    return out

def _table(hdr, rows):
    cols = []  # (idx, kind, quant_prefix)
    for k, h in enumerate(hdr):
        if not SPEED_H.search(h): continue
        if re.search(r"J/tok|latency|vs off|ms\b", h, re.I): continue
        kind = "prefill" if PRE_H.search(h) else "gen"
        qm = QUANT.search(h.replace("TG", " TG").replace("PP", " PP"))
        cols.append((k, kind, qm.group(0) if qm and not re.match(r"(?i)^(tg|pp)", qm.group(0)) else None))
    out = []
    if cols:
        for r in rows:
            c = split_row(r)
            label = " ".join(x for k, x in enumerate(c) if k not in [q[0] for q in cols] and num(x) is None)
            label_clean = re.sub(r"\]\([^)]*\)|[\[\]`*]", " ", label)
            hm = HW.search(label_clean); qm = QUANT.search(label_clean)
            groups = {}
            for k, kind, qp in cols:
                if k >= len(c): continue
                v = num(c[k])
                if v is None: continue
                groups.setdefault(qp, {})[kind] = v
            for qp, g in groups.items():
                out.append(dict(hardware=hm.group(0).strip() if hm else None, quant=qp or (qm.group(0) if qm else None),
                                label=re.sub(r"\s+", " ", label_clean).strip()[:80], gen=g.get("gen"), prefill=g.get("prefill"), raw=r.strip()[:300]))
        return out
    # 键值表：| 测试 | 12.3 tok/s |
    for r in rows:
        c = split_row(r)
        if len(c) < 2: continue
        m = VAL_SPEED.search(c[1])
        if not m or not re.match(r"^\s*~?\d", c[1]): continue
        v = float(m.group(1).replace(",", ""))
        kind = "prefill" if PRE_H.search(c[0]) else "gen"
        hm = HW.search(c[0])
        out.append(dict(hardware=hm.group(0).strip() if hm else None, quant=None, label=c[0][:80],
                        gen=v if kind == "gen" else None, prefill=v if kind == "prefill" else None, raw=r.strip()[:300]))
    return out

def sentence_speeds(text):
    """表格之外的句子：同一句同时有数字 tok/s 和硬件才算"""
    out = []
    for s in re.split(r"(?<=[.;])\s+|\n", text):
        if s.strip().startswith("|"): continue
        hm = HW.search(s); m = VAL_SPEED.search(s)
        if hm and m and not PRE_H.search(s[:m.start()][-40:]):
            out.append(dict(hardware=hm.group(0).strip(), quant=None, label="sentence", gen=float(m.group(1).replace(",", "")), prefill=None, raw=s.strip()[:300]))
    return out

def extract(model_id, text, include_nonconsumer=False):
    rows = parse_tables(text)
    from_tables = bool(rows)
    if not rows: rows = sentence_speeds(text)
    decl = declared_hardware(text)
    card_hw = next((h for h in decl if not re.match(r"(?i)^M[1-5]$", h)), None)
    for r in rows:
        if not r["hardware"]: r["hardware"] = card_hw; r["hardware_from"] = "declaration" if card_hw else None
        else: r["hardware_from"] = "row"
        r["hw_class"] = hw_class(r["hardware"])
        r["excluded"] = (not include_nonconsumer) and r["hw_class"] in ("datacenter", "workstation")
    caveats = list(dict.fromkeys(m.group(0) for m in CAVEAT.finditer(text)))
    flags = []
    name = model_id.split("/")[-1]
    if re.search(r"(?i)\bocr\b|embedding|rerank|whisper|\btts\b", name) or re.search(r"(?i)\bOCR\b", text[:400]): flags.append("非通用 LLM（OCR/嵌入/语音）")
    sz = re.search(r"(?i)(?<![\d.])(\d+(?:\.\d+)?)B(?:-|_|\b)", name)
    if sz and float(sz.group(1)) < 3: flags.append("<3B 小模型")
    if PLACEHOLDER.search(text): flags.append("含占位链接")
    if not from_tables and rows: flags.append("仅句子抽取")
    kept = [r for r in rows if not r["excluded"]]
    gen_rows = [r for r in kept if r["gen"] is not None]
    primary = gen_rows[0] if gen_rows else None
    conf = 0.2 + 0.3 * bool(primary) + 0.2 * bool(primary and primary["hardware"]) + 0.15 * from_tables + 0.15 * bool(primary and primary["quant"])
    conf = round(max(0.05, conf - 0.3 * len(flags)), 2)
    fp = hashlib.sha1(repr(sorted((r["hardware"] or "", r["gen"] or 0, r["prefill"] or 0) for r in rows)).encode()).hexdigest()[:12] if rows else None
    return dict(rows=rows, primary=primary, context_tokens=ctx_tokens(text), caveats=caveats, flags=flags,
                confidence=conf, table_fingerprint=fp, declared_hardware=decl)
