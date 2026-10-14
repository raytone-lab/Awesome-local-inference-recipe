"""模型卡测速抽取（纯函数，便于测试）。v3 规则（2026-10-14）：
表格
- 逐行解析：一行 = 硬件 × 量化/配置；按表头区分 生成 / 读入 / 聚合吞吐(并发) / 峰值；延迟列(TTFT/TPOT/ms/latency)忽略
- 表头没有 tok/s 但单元格带单位（"33.1 tokens/s"）的列也算速度列；表头的 decode/prefill/generation 词决定类别
- 对照列（FP16/BF16/4-bit/8-bit 基线、original/reference）跳过；同一表多个生成列（如 投机 关/开、new text/code）拆成多条，variant=列名
- 转置表（首列是 "Token generation / Prompt processing / Generation (mean of 6)" 等指标名）：按列出记录；
  若列名不像配置开关（on/off/with/without/MTP/spec/helper），只取第一列（其余视为对比模型）
- 评测/任务表（Task|Verdict|PASS|ID）与延迟表（arrival rate / TTFT p50 / TPOT）整体跳过
- 单元格支持 "**283 tok/s**[^x]"、"14.9–17.7 tok/s"（取下限，保留区间）、"113 / 140 tok/s"（冷/热，读入取后者）、"~2,670 tok/s @ bs 32"
- 行内上下文（"4k tokens of context"、"16,384" 在 prompt/context 列）写入 row.context_tokens，不污染卡级上下文
硬件
- 行标签 > 表前最近的硬件提及（含 "## Measured" 标题后首行、"Machine:"、"Hardware:"）> 卡级声明句 > 表后声明句
- 机房卡/服务器 CPU（H100/A100/L40S/L4/Xeon/EPYC…）与工作站卡（RTX PRO/RTX 6000 Ada/A6000）默认排除
来源与说明
- 表前文字或列名出现 "their numbers / not ours / community benchmark / X's numbers / by <name>" → 该表行 level=转述
- "up to" 峰值说法 → row.peak_claim=True 并进 caveats；pending re-measurement 等保留说明进 caveats
- 句子抽取：段落合并后，同句有硬件+速度才算；取离硬件最近的速度数字
其他
- OCR/嵌入/语音、<3B、占位链接 → flags 降分；flags 含「非通用 LLM」时 primary=None（交给过滤）
- 行级 dup_key 供跨卡去重（seen_rows 参数；ingest_hf.py 会把历史候选批次的 dup_key 一并载入）
v4 增补（2026-10-14）
- 对照列：成对列 "A tg | B tg" 中，A 在卡内写作 "vs (uniform) A" → 跳过 A；表头裸 tg/pp 也算速度列
- 多档上下文表有 Mean/Average/Median 行时只取汇总行
- Bits/Weight、bpw 列 → quant 写成 "<行名> (<bpw> bpw)"（如 byteshape 的 GPU-1..5 是量化档 ID）
- Headline/Highlights 表 → peak_claim=True，primary 优先非峰值行；"prose **140**, code 209" 取 prose 值
- 前缀配对：多生成列时 "X prefill" 只配 "X decode"
- 硬件补 RTX A 系列 / A6000（工作站，默认排除）、Radeon AI PRO R9700、Radeon RX
- 噪声：encoder/embedding throughput、tokens per second of video/audio 整行丢弃
- 句子：链接到别的 HF 模型的句子丢弃；列表项各自成句；优先取数字前面最近的硬件"""
import re, hashlib

DC = re.compile(r"\b(H100|H200|H20|B200|B300|GB200|A100|A800|L40S?|L4\b|A10G?|T4\b|MI300X?|MI325X?|Gaudi|Xeon|EPYC|Threadripper)", re.I)
WS = re.compile(r"\b(Radeon\s(?:AI\s)?PRO\s?W\d{4}|RTX\s?PRO\s?\d{4}|RTX\s?6000(?:\s?Ada)?|RTX\s?A\d{4}|A6000|RTX\s?[45]000\s?Ada)", re.I)
HW = re.compile(r"(RTX\s?A\d{4}(?:\s?Ada)?(?:,?\s?\d+\s?GB)?|\bA6000\b|Radeon\s(?:AI\s)?PRO\s?(?:R|W)\d{4}(?:,?\s?\d+\s?GB)?|Radeon\s?(?:RX\s?)?\d{4}\s?(?:XTX|XT|GRE)?|RTX\s?PRO\s?\d{4}(?:\s?Blackwell)?(?:\s?SFF(?:\s?Edition)?)?|RTX\s?\d{4}(?:\s?(?:Ti|SUPER))?(?:\s?Ada)?(?:\s?Laptop)?(?:\s?\(?\d+\s?GB\)?)?|\b[2-5]0[6-9]0(?:\s?(?:Ti|SUPER))?\b|(?:Tesla\s)?V100(?:\s?\d+\s?GB)?|\bP40\b|\bMI50\b|\bMI60\b|7900\s?XTX|Strix Halo|DGX Spark|\bH100(?:\s?(?:SXM|NVL|PCIe))?|\bA100(?:\s?SXM)?|\bL40S?\b|\bL4\b|Xeon|EPYC|iPhone\s?\d+(?:\s?Pro(?:\s?Max)?)?|Samsung\s?S\d+\s?Ultra|(?:Apple\s)?M[1-5]\s?(?:Pro|Max|Ultra)\b(?:,?\s?\d+\s?GB)?|Mac\s?(?:Studio|mini)(?:\s?M[1-5](?:\s?(?:Pro|Max|Ultra))?)?(?:,?\s?\d+\s?GB)?)", re.I)
QUANT = re.compile(r"\b(?:UD-)?(?:P?T?I?Q\d(?:_[0-9A-Z]+)*|MXFP4|NVFP4|FP8|BF16|F16|GPTQ-Int4|AWQ|EXL[23]|\d-bit)\b", re.I)
GEN_W = re.compile(r"\btg\d+\b|decode|generat|\beval\b|output|writing speed|生成|tok/s|t/s|tokens?/s|\btps\b|throughput|speed", re.I)
PRE_W = re.compile(r"\bpp\d*\b|prefill|prompt (?:processing|ingestion|t/s|tok)|prompt\b(?! tokens)|ingest|读入|reading", re.I)
AGG_W = re.compile(r"aggregate|server throughput|batch|\bbs\s?\d|concurren|streams", re.I)
PEAK_W = re.compile(r"\bpeak\b|\bmax\b", re.I)
SKIP_COL = re.compile(r"J/tok|latency|TTFT|TPOT|\bms\b|vs off|speedup|\bvs\b|ratio|accept|VRAM|memory|size|footprint|\bGB\b|KL\b|checks|pass|%", re.I)
BASE_COL = re.compile(r"\b(FP16|BF16|F16|fp16)\b|\b[48]-bit\b|original|reference|\bref\b|baseline\b(?!.*(spec|no-?spec))", re.I)
VARIANT = re.compile(r"\bon\b|\boff\b|with|without|\bno\b|MTP|spec|helper|draft|DFlash|baseline|autoregressive|new text|code|cold|warm", re.I)
SKIP_TABLE = re.compile(r"\bverdict\b|\btask\b.*\b(pass|verdict|kw)|arrival rate|TTFT p\d|TPOT p\d|\|\s*ID\s*\|", re.I)
UNIT = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(?:[–\-~]\s*(\d[\d,]*(?:\.\d+)?))?\s*(?:/\s*(\d[\d,]*(?:\.\d+)?)\s*)?(?:tok/s|t/s|tokens?/s(?:ec)?|tokens per second)", re.I)
DECL = re.compile(r"(measured (?:on|with)|hardware:|machine:|gpu0:|tested on|on (?:one|an?|my|our|the same|two) |decode speed on|benchmarked on|## measured)", re.I)
THIRD = re.compile(r"their numbers|not ours|community (?:user|benchmark|tester)|'s numbers|reported by|— by [A-Z]|benchmark(?:ed)? by", re.I)
CAVEAT = re.compile(r"(pending re-?measurement|not a specification|thermally limited|separate measurements|not the same run|our numbers on our box|earlier .{0,20}build|estimates? rather than|not a benchmark|up to \**\d[\d,.]*\**\s*(?:tok|t/s|tokens))", re.I)
CTX = re.compile(r"(?:ctx-size|context(?:\s+length|\s+window)?|上下文)[^\n\d]{0,30}?(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?\s?[KkM]\b|\d{4,7})|(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?\s?[KkM])[- ](?:token )?context", re.I)
PLACEHOLDER = re.compile(r"github\.com/your-org|github\.com/USERNAME|example\.com/", re.I)
NOISE = re.compile(r"encoder throughput|embedding throughput|tokens? per second of (?:video|audio)|tokens?/s of (?:video|audio)", re.I)
SEP = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")

def clean(s): return re.sub(r"\[\^[^\]]*\]|[`*¹²³⁴]|\\", "", s).strip()

def parse_cell(s):
    """返回 (value, low, high, slash_vals) 或 None"""
    s = clean(s)
    if not s or s in ("—", "-", "–"): return None
    s = re.sub(r"^(?:prose|text|chat|general)\s+(?=\d)", "", s, flags=re.I)
    m = UNIT.search(s)
    if m:
        a = float(m.group(1).replace(",", ""))
        b = float(m.group(2).replace(",", "")) if m.group(2) else None
        c = float(m.group(3).replace(",", "")) if m.group(3) else None
        return dict(v=a, hi=b, slash=c, unit=True)
    m = re.match(r"^~?\s*(\d[\d,]*(?:\.\d+)?)\s*(?:[–\-]\s*(\d[\d,]*(?:\.\d+)?))?\s*(?:/\s*(\d[\d,]*(?:\.\d+)?))?\s*(?:\(.*\))?\s*(?:mean.*|,.*)?$", s)
    if m:
        return dict(v=float(m.group(1).replace(",", "")), hi=float(m.group(2).replace(",", "")) if m.group(2) else None,
                    slash=float(m.group(3).replace(",", "")) if m.group(3) else None, unit=False)
    return None

def num(s):
    p = parse_cell(s); return p["v"] if p else None

def hw_class(hw):
    if not hw: return None
    if DC.search(hw): return "datacenter"
    if WS.search(hw): return "workstation"
    return "consumer"

def tokens_of(v):
    v = v.replace(",", "").replace(" ", "")
    try: n = float(v[:-1]) * (1024 if v[-1] in "Kk" else 1024 ** 2) if v[-1] in "KkM" else float(v)
    except (ValueError, IndexError): return None
    return int(n)

def ctx_tokens(text):
    best = None
    for line in text.splitlines():
        if line.strip().startswith("|"): continue
        for m in CTX.finditer(line):
            n = tokens_of(m.group(1) or m.group(2) or "")
            if n and 2048 <= n <= 10_000_000: best = max(best or 0, n)
    return best

def find_hw(s):
    m = HW.search(s); return re.sub(r"\s+", " ", m.group(0)).strip(" ,(") if m else None

def declared_hardware(text):
    hws, lines = [], text.splitlines()
    for i, line in enumerate(lines):
        if DECL.search(line):
            seg = line + (" " + lines[i + 1] if line.strip().startswith("#") and i + 1 < len(lines) else "")
            for m in HW.finditer(seg):
                h = re.sub(r"\s+", " ", m.group(0)).strip(" ,(")
                if h not in hws: hws.append(h)
    return hws

def split_row(l): return [c.strip() for c in l.strip().strip("|").split("|")]

def iter_tables(text):
    lines, i = text.splitlines(), 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and SEP.match(lines[i + 1]):
            j = i + 2; rows = []
            while j < len(lines) and lines[j].strip().startswith("|"): rows.append(lines[j]); j += 1
            k = i - 1; before = []
            while k >= 0 and len(before) < 6 and not lines[k].strip().startswith("|"):
                if lines[k].strip(): before.insert(0, lines[k])
                if lines[k].lstrip().startswith("#"): break
                k -= 1
            after = [l for l in lines[j:j + 4] if l.strip() and not l.strip().startswith("|")]
            yield split_row(lines[i]), rows, before, after
            i = j; continue
        i += 1

def row_ctx(label, hdr0):
    m = re.search(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?\s?[kK])\b", label)
    if m and (re.search(r"context|prompt|token|ctx", label + " " + hdr0, re.I) or re.fullmatch(r"\s*\d+(?:\.\d+)?\s?[kK]\s*", label)):
        n = tokens_of(m.group(1)); return n if n and n >= 512 else None
    return None

def col_kind(h, cells, ncols=2):
    hc = clean(h)
    unit_cells = sum(bool(UNIT.search(clean(c))) for c in cells)
    nonempty = sum(bool(clean(c)) and clean(c) not in ("—", "-") for c in cells)
    if ncols > 2 and unit_cells and unit_cells * 2 < nonempty and not re.search(r"t/s|tok/s|tokens?/s|\btps\b|\btg\d+\b|\bpp\d+\b|decode|prefill|speed", hc, re.I): return None
    has_speed_hdr = bool(re.search(r"t/s|tok/s|tokens?/s|\btps\b|\btg\d*\b|\bpp\d*\b", hc, re.I))
    if not has_speed_hdr and not unit_cells and not re.search(r"decode|prefill|generation|writing speed", hc, re.I): return None
    if not has_speed_hdr and not unit_cells and re.search(r"rows|count|n_dec|\blen\b|tokens\b|time|\(s\)", hc, re.I): return None
    if not has_speed_hdr and not unit_cells: return None if not any(num(c) is not None for c in cells) else ("gen" if not PRE_W.search(hc) else "prefill")
    if SKIP_COL.search(hc) and not has_speed_hdr and not unit_cells: return None
    if re.search(r"TTFT|TPOT|latency|J/tok|speedup|vs off|ratio", hc, re.I): return None
    if PRE_W.search(hc): return "prefill"
    if AGG_W.search(hc): return "agg"
    if PEAK_W.search(hc) and not re.search(r"memory|vram", hc, re.I): return "peak"
    return "gen"

def is_comparator(h, card_text):
    """列名前缀是卡内写明的对照组（"vs uniform oQ4e"）→ 对照列"""
    toks = clean(h).split()
    if len(toks) < 2 or re.match(r"(?i)^(tg|pp|tps|tok|t/s|decode|prefill|gen|speed)", toks[0]): return False
    t = re.escape(toks[0])
    return bool(re.search(rf"\bvs\.?\s+(?:uniform\s+|the\s+|stock\s+|plain\s+)?{t}\b|\buniform\s+{t}\b", card_text, re.I))

def _table(hdr, rows, before, after, ctx_hw, third_default, card_text=""):
    head = " ".join(hdr)
    if SKIP_TABLE.search("| " + " | ".join(hdr) + " |"): return []
    ctx_text = " ".join(before)
    third = third_default or bool(THIRD.search(ctx_text))
    local_hw = next((find_hw(l) for l in reversed(before) if DECL.search(l) and find_hw(l)), None) \
        or next((find_hw(l) for l in reversed(before) if find_hw(l)), None)
    cells = [split_row(r) for r in rows]
    agg_rows = [c for c in cells if c and re.fullmatch(r"(?i)mean|average|avg|median", clean(c[0]))]
    if agg_rows and len(cells) > 2: cells = agg_rows  # 多档上下文表：只取 Mean 汇总行
    bpw_col = next((k for k, h in enumerate(hdr) if re.search(r"(?i)bits\s*/\s*weight|\bbpw\b", clean(h))), None)
    headline = bool(re.match(r"(?i)(headline|highlights?|at a glance)\b", clean(hdr[0]))) if hdr else False
    out = []
    # 转置表：首列是指标名
    metric_rows = [c for c in cells if c and re.match(r"(?:\w+\s)?(token generation|prompt processing|generat\w*|decode|prefill|prompt|tg\d+|pp\d+)\b", clean(c[0]), re.I)]
    if metric_rows and (len(metric_rows) * 2 >= len(cells) or not re.search(r"t/s|tok/s|tokens?/s|tg\d|pp\d", " ".join(hdr[1:]), re.I)) and not re.search(r"t/s|tok/s|tg\d|pp\d|decode|prefill", clean(hdr[0]), re.I) and len(hdr) >= 2 and not find_hw(" ".join(clean(c[0]) for c in cells)):
        vcols = [k for k in range(1, len(hdr)) if not BASE_COL.search(clean(hdr[k]))]
        if len([k for k in vcols if VARIANT.search(clean(hdr[k]))]) < 2: vcols = vcols[:1]
        for k in vcols:
            rec = dict(gen=None, prefill=None, variant=clean(hdr[k])[:60])
            for c in cells:
                if k >= len(c): continue
                p = parse_cell(c[k]); lab = clean(c[0])
                if not p or re.search(r"TTFT|latency|time|vram|memory|accept", lab, re.I): continue
                if PRE_W.search(lab) and rec["prefill"] is None: rec["prefill"] = p["slash"] or p["v"]
                elif re.search(r"generat|decode|tg\d|writing", lab, re.I) and rec["gen"] is None and not re.search(r"after|at \d|\d+k", lab, re.I):
                    rec["gen"] = p["v"]; rec["gen_hi"] = p["hi"]; rec["raw"] = "| " + " | ".join(c) + " |"
            if rec["gen"] is None and rec["prefill"] is None: continue
            hw = find_hw(clean(hdr[k])) or local_hw or ctx_hw
            cell_hw = next((find_hw(clean(c[k])) for c in metric_rows if k < len(c) and find_hw(clean(c[k]))), None)
            out.append(dict(hardware=cell_hw or hw, quant=(QUANT.search(clean(hdr[k])) or [None])[0], label=clean(c[0])[:60],
                            raw=rec.get("raw", rows[0].strip())[:300], level="转述" if (third or THIRD.search(hdr[k])) else None,
                            context_tokens=None, aggregate=None, peak=None, **{k2: rec.get(k2) for k2 in ("gen", "prefill", "variant", "gen_hi")}))
        return out
    kinds = [col_kind(h, [c[k] if k < len(c) else "" for c in cells], len(hdr)) for k, h in enumerate(hdr)]
    sfx = lambda k: " ".join(clean(hdr[k]).lower().split()[1:])
    comp = {k for k, t in enumerate(kinds) if t in ("gen", "prefill") and is_comparator(hdr[k], card_text)
            and any(k2 != k and t2 == t and sfx(k2) == sfx(k) for k2, t2 in enumerate(kinds))}  # 只在 "A tg | B tg" 成对列时判对照
    if comp and any(t == "gen" and k not in comp for k, t in enumerate(kinds)): kinds = [None if k in comp else t for k, t in enumerate(kinds)]
    gen_cols = [k for k, t in enumerate(kinds) if t == "gen" and not (BASE_COL.search(clean(hdr[k])) and any(t2 == "gen" and not BASE_COL.search(clean(hdr[k2])) for k2, t2 in enumerate(kinds) if k2 != k))]
    pre_cols = [k for k, t in enumerate(kinds) if t == "prefill" and not BASE_COL.search(clean(hdr[k]))]
    agg_cols = [k for k, t in enumerate(kinds) if t == "agg"]
    peak_cols = [k for k, t in enumerate(kinds) if t == "peak"]
    if not (gen_cols or pre_cols or agg_cols): return []
    # 量化前缀分组（"PQ2_0 TG128 | PTQ1_0 TG128"）
    def qp(k):
        m = QUANT.search(clean(hdr[k]).replace("TG", " TG").replace("PP", " PP"))
        return m.group(0) if m and not re.match(r"(?i)^(tg|pp)", m.group(0)) else None
    groups = {}
    for k in gen_cols: groups.setdefault(qp(k), {"gen": [], "pre": []})["gen"].append(k)
    for k in pre_cols: groups.setdefault(qp(k), {"gen": [], "pre": []})["pre"].append(k)
    used = set(gen_cols + pre_cols + agg_cols + peak_cols)
    for c in cells:
        label = " ".join(x for k, x in enumerate(c) if k not in used and (kinds[k] is None) and num(x) is None and not re.search(r"^\d", clean(x)))
        if not label: label = c[0] if c else ""
        lc = re.sub(r"\]\([^)]*\)|[\[\]`*]", " ", label); lc = re.sub(r"\s+", " ", lc).strip()
        rh = find_hw(clean(c[0])) if c else None
        rq = (QUANT.search(lc) or [None])[0]
        rctx = row_ctx(clean(c[0]) if c else "", hdr[0])
        agg = next((parse_cell(c[k])["v"] for k in agg_cols if k < len(c) and parse_cell(c[k])), None)
        pk = next((parse_cell(c[k])["v"] for k in peak_cols if k < len(c) and parse_cell(c[k])), None)
        for q, g in groups.items():
            pre = None
            for k in g["pre"]:
                p = parse_cell(c[k]) if k < len(c) else None
                if p: pre = p["slash"] or p["v"]; break
            gcols = g["gen"] or [None]
            multi = len([k for k in gcols if k is not None]) > 1
            for k in gcols:
                p = parse_cell(c[k]) if k is not None and k < len(c) else None
                if p and not multi and not g["pre"] and c and PRE_W.search(clean(c[0])) and not re.search(r"decode|generat", clean(c[0]), re.I):
                    pre, p = (p["slash"] or p["v"]), None
                pre_k = pre
                if multi and k is not None and g["pre"]:  # "Gyro-S prefill" 只配 "Gyro-S decode"，不配 "Gyro-M decode"
                    f0 = lambda kk: clean(hdr[kk]).split()[0].lower() if clean(hdr[kk]).split() else ""
                    if any(f0(kp) == f0(k2) for kp in g["pre"] for k2 in gcols if k2 is not None) and not any(f0(kp) == f0(k) for kp in g["pre"]): pre_k = None
                if p is None and pre_k is None and agg is None: continue
                if k is not None and p is None and multi: continue
                cell_hw = find_hw(clean(c[k])) if p and k is not None else None
                hw = rh or cell_hw or local_hw or ctx_hw
                bq = None
                if bpw_col is not None and bpw_col < len(c) and num(c[bpw_col]) is not None: bq = f"{clean(c[0])} ({num(c[bpw_col])} bpw)"
                out.append(dict(hardware=hw, quant=q or rq or bq, label=lc[:80], peak_claim=headline, gen=p["v"] if p else None, gen_hi=p["hi"] if p else None,
                                prefill=pre_k, aggregate=agg, peak=pk, variant=clean(hdr[k])[:60] if multi and k is not None else None,
                                context_tokens=rctx, level="转述" if (third or THIRD.search(head)) else None, raw=("| " + " | ".join(c) + " |")[:300]))
    return out

def parse_tables(text, ctx_hw=None):
    out = []
    for hdr, rows, before, after in iter_tables(text):
        hw_after = next((find_hw(l) for l in after if DECL.search(l) and find_hw(l)), None)
        out += _table(hdr, rows, before, after, ctx_hw or hw_after, False, text)
    return out

def sentence_speeds(text, model_id=None):
    out = []
    paras = re.split(r"\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)", text)  # 列表项各自成段
    for para in paras:
        if para.strip().startswith("|"): continue
        flat = re.sub(r"\s*\n\s*", " ", para)
        for s in re.split(r"(?<=[.;])\s+(?=[A-Z(\[*`])", flat):
            hms = list(HW.finditer(s)); ums = list(UNIT.finditer(s))
            if not hms or not ums: continue
            links = re.findall(r"huggingface\.co/([\w.\-]+/[\w.\-]+)", s)
            if model_id and any(l.lower() != model_id.lower() for l in links): continue  # 句中链接到别的模型，数值归属不明
            after = [(h.start() - u.end(), u, h) for u in ums for h in hms
                     if 0 <= h.start() - u.end() <= 30 and re.match(r"[\s*]*(?:on|with|using)\b", s[u.end():h.start()], re.I)]  # "44 tok/s on an M5 Pro"
            pairs = after or [(u.start() - h.start(), u, h) for u in ums for h in hms if h.start() < u.start()] or [(abs(u.start() - h.start()), u, h) for u in ums for h in hms if abs(u.start() - h.start()) <= 80]
            if not pairs: continue
            best = min(pairs, key=lambda x: x[0])
            _, u, h = best
            pre = s[max(0, u.start() - 40):u.start()]
            if PRE_W.search(pre) and not GEN_W.search(pre[-15:]): continue
            out.append(dict(hardware=re.sub(r"\s+", " ", h.group(0)).strip(" ,("), quant=None, label="sentence",
                            gen=float(u.group(1).replace(",", "")), gen_hi=float(u.group(2).replace(",", "")) if u.group(2) else None,
                            prefill=None, aggregate=None, peak=None, variant=None, context_tokens=None,
                            peak_claim=bool(re.search(r"up to\s*\**\s*$", s[:u.start()][-12:], re.I)),
                            level="转述" if THIRD.search(s) else None, raw=s.strip()[:300]))
    return out

def extract(model_id, text, include_nonconsumer=False, seen_rows=None):
    decl = declared_hardware(text)
    card_hw = next((h for h in decl if not re.match(r"(?i)^M[1-5]$", h)), None)
    rows = parse_tables(text)
    from_tables = bool([r for r in rows if r["gen"] is not None])
    sent = sentence_speeds(text, model_id)
    if not from_tables: rows += sent
    else:
        known = {r["gen"] for r in rows}
        rows += [s for s in sent if s["gen"] not in known and DECL.search(s["raw"])]
    rows = [r for r in rows if not NOISE.search(r["raw"])]
    for r in rows:
        r.setdefault("peak_claim", False)
        if not r["hardware"]: r["hardware"] = card_hw; r["hardware_from"] = "declaration" if card_hw else None
        else: r["hardware_from"] = r.get("hardware_from") or "row/context"
        r["hw_class"] = hw_class(r["hardware"])
        r["excluded"] = (not include_nonconsumer) and r["hw_class"] in ("datacenter", "workstation")
        r["level"] = r.get("level") or "宣称"
        r["dup_key"] = f"{(r['hardware'] or '').lower()}|{r['gen']}|{r['prefill']}|{(r['label'] or '')[:40].lower()}"
        r["duplicate"] = bool(seen_rows is not None and r["gen"] is not None and r["dup_key"] in seen_rows)
    caveats = list(dict.fromkeys(m.group(0) for m in CAVEAT.finditer(text)))
    flags = []
    name = model_id.split("/")[-1]
    if re.search(r"(?i)(^|[-_])ocr([-_]|$)|\bocr\b|embedding|rerank|whisper|\btts\b", name) or re.search(r"(?i)\bOCR\b", text[:400]): flags.append("非通用 LLM（OCR/嵌入/语音）")
    sz = re.search(r"(?i)(?<![\d.])(\d+(?:\.\d+)?)B(?:-|_|\b)", name)
    if sz and float(sz.group(1)) < 3: flags.append("<3B 小模型")
    if PLACEHOLDER.search(text): flags.append("含占位链接")
    if not from_tables and rows: flags.append("仅句子抽取")
    kept = [r for r in rows if not r["excluded"] and not r["duplicate"]]
    gen_rows = [r for r in kept if r["gen"] is not None]
    rank = lambda r: (r["level"] == "转述", r["hw_class"] in ("datacenter", "workstation"), bool(r.get("peak_claim")))
    primary = sorted(gen_rows, key=rank)[0] if gen_rows else None
    if any("非通用" in f for f in flags): primary = None
    conf = 0.2 + 0.3 * bool(primary) + 0.2 * bool(primary and primary["hardware"]) + 0.15 * from_tables + 0.15 * bool(primary and primary["quant"])
    conf = round(max(0.05, conf - 0.3 * len(flags) - 0.1 * bool(primary and primary.get("peak_claim"))), 2)
    fp = hashlib.sha1(repr(sorted((r["hardware"] or "", r["gen"] or 0, r["prefill"] or 0) for r in rows)).encode()).hexdigest()[:12] if rows else None
    if seen_rows is not None: seen_rows.update(r["dup_key"] for r in rows if r["gen"] is not None)
    return dict(rows=rows, primary=primary, context_tokens=ctx_tokens(text), caveats=caveats, flags=flags,
                confidence=conf, table_fingerprint=fp, declared_hardware=decl)
