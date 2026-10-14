"""2026-10-14 批次 29 张卡的回归测试（金标准为人工审核结果）"""
import os, sys, unittest
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "scripts"))
from hf_extract import extract, parse_cell
def run(n, **k):
    with open(os.path.join(H, "fixtures", "hf", n + ".md")) as f: return extract(n.replace("_", "/", 1), f.read(), **k)
def rows(e, hw=None, gen=None):
    return [r for r in e["rows"] if (hw is None or (r["hardware"] and hw.lower() in r["hardware"].lower())) and (gen is None or r["gen"] == gen)]

class Cells(unittest.TestCase):
    def test_formats(self):
        self.assertEqual(parse_cell("**283 tok/s**[^int8on]")["v"], 283)
        p = parse_cell("14.9–17.7 tok/s"); self.assertEqual((p["v"], p["hi"]), (14.9, 17.7))
        self.assertEqual(parse_cell("113 / 140 tok/s")["slash"], 140)
        self.assertEqual(parse_cell("**~2,670 tok/s** @ bs 32")["v"], 2670)
        self.assertEqual(parse_cell("**10 tokens/s**")["v"], 10)

class Batch2(unittest.TestCase):
    def test_baseline_cols_skipped(self):
        e = run("prism-ml_Bonsai-8B-gguf")
        self.assertEqual(rows(e, "4090")[0]["gen"], 368); self.assertEqual(rows(e, "4090")[0]["prefill"], 11809)
        self.assertNotIn(59, [r["gen"] for r in e["rows"]])
        self.assertTrue(rows(e, "L40S")[0]["excluded"])
        self.assertEqual(rows(e, "Samsung")[0]["gen"], 19.6)
        self.assertEqual(run("prism-ml_Ternary-Bonsai-8B-mlx-2bit")["primary"]["gen"], 83)
    def test_transposed(self):
        e = run("prism-ml_Bonsai-8B-mlx-1bit"); r = rows(e, "iPhone")[0]
        self.assertEqual((r["gen"], r["prefill"]), (44, 377))
        self.assertNotIn(14, [x["gen"] for x in e["rows"]])  # 4-bit 对照列
        k = run("Kujira_Underdog-Saluki-27B-1.0-MTP-GGUF")
        self.assertEqual([r["gen"] for r in k["rows"] if r["label"] != "sentence"][:2], [40.7, 66.2])
        self.assertIn("3080", k["primary"]["hardware"])
        p = run("FINAL-Bench_POCKET-35B-GGUF"); self.assertEqual(p["primary"]["gen"], 25.4); self.assertIn("M3 Pro", p["primary"]["hardware"])
        self.assertTrue(rows(p, "Xeon")[0]["excluded"])
    def test_slash_and_range(self):
        e = run("Edge0_Edge0-35B-A3B-preview"); self.assertEqual((e["primary"]["gen"], e["primary"]["prefill"], e["primary"]["gen_hi"]), (14.9, 140, 17.7))
        self.assertIn("Mac mini", e["primary"]["hardware"])
        e = run("Edge0_Edge0-8B-A1B-preview"); self.assertEqual((e["primary"]["gen"], e["primary"]["prefill"]), (23.9, 1428))
    def test_latency_and_aggregate(self):
        e = run("EschaLabs_Qwen3.6-35B-A3B-Escha-W2")
        self.assertEqual(e["primary"]["gen"], 283); self.assertNotIn(445, [r["gen"] for r in e["rows"]])
        self.assertEqual({r["hardware"]: r["gen"] for r in e["rows"][:5]}, {"RTX 5090": 283, "RTX 4090": 225, "RTX 5080": 212, "RTX 3090": 154, "RTX 5060 Ti": 128})
        self.assertEqual(rows(e, "RTX 4090", 225)[0]["aggregate"], 1321)
    def test_eval_table_skipped(self):
        e = run("cloudyu_gpt-oss-120b-Fable-5-Distilled"); self.assertEqual(e["primary"]["gen"], 12)
    def test_spec_on_off_pairs(self):
        e = run("meta-models_Muse-Glimmer-30B-GGUF")
        self.assertEqual([r["gen"] for r in rows(e, "5090")], [74.9, 233.4]); self.assertEqual(e["primary"]["gen"], 74.9)
        u = run("ConwayResearch_Underdog-27B-1.0"); self.assertEqual([r["gen"] for r in u["rows"][:2]], [33.1, 80.6]); self.assertIn("M5 Max", u["primary"]["hardware"])
        a = run("mlx-community_AREX-2-6bit"); self.assertIn(10, [r["gen"] for r in a["rows"]]); self.assertTrue(any("not a benchmark" in c for c in a["caveats"]))
    def test_machine_heading(self):
        e = run("OpensourceWTF_DeepSeek-V4.1-Flash-streaming-repack-exl3-3.0bpw")
        self.assertIn("M5 Max", e["primary"]["hardware"]); self.assertEqual(e["primary"]["gen"], 39.9)
        self.assertNotIn(167, [r["gen"] for r in e["rows"]])
        self.assertEqual(rows(e, gen=11.1)[0]["context_tokens"], 1047488)
    def test_row_context(self):
        e = run("CaryPalmer_Ternary-Bonsai-2-27B-262k-GGUF")
        self.assertEqual(rows(e, "4070", 102)[0]["context_tokens"], 4096)
        self.assertEqual(rows(e, "4070", 78)[0]["prefill"], 1031)
        self.assertIn(8.6, [r["gen"] for r in e["rows"]]); self.assertIn(51.2, [r["gen"] for r in e["rows"]])
        self.assertNotEqual(e["context_tokens"], 4096)
    def test_third_party(self):
        e = run("esatapedico_Qwen3.8-27B-NVFP4-MTP-GGUF")
        r = rows(e, "5090", 148.3)[0]; self.assertEqual(r["level"], "转述"); self.assertEqual(r["peak"], 203)
        self.assertEqual(e["primary"]["gen"], 18.44); self.assertEqual(e["primary"]["level"], "宣称")
        self.assertEqual(rows(e, gen=25.98)[0]["level"], "宣称")
    def test_peak_claims(self):
        g = run("manjunathshiva_gpt-oss-20b-tq3"); self.assertEqual(g["primary"]["gen"], 73); self.assertTrue(g["primary"]["peak_claim"])
        m = run("peasantsmith_GLM-5.3-Flash-Maya-GGUF"); self.assertEqual([r["gen"] for r in m["rows"]], [40, 19]); self.assertTrue(all(r["peak_claim"] for r in m["rows"]))
        self.assertIn("V100", m["primary"]["hardware"])
    def test_mtplx(self):
        e = run("Youssofal_Qwen3.8-Flash-Next-MTPLX-Optimized-Speed")
        for v in (73.5, 43.8, 50.3): self.assertIn(v, [r["gen"] for r in e["rows"]])
        self.assertIn(1453, [r["prefill"] for r in e["rows"]])
    def test_cross_card_dedupe(self):
        seen = set(); run("prism-ml_Ternary-Bonsai-27B-mlx-2bit", seen_rows=seen)
        d = run("prism-ml_Ternary-Bonsai-27B-gguf", seen_rows=seen); self.assertIsNone(d["primary"])
        seen = set(); run("Youssofal_Qwen3.8-27B-MTPLX-Optimized-Speed", seen_rows=seen)
        q = run("Youssofal_Qwen3.8-27B-MTPLX-Optimized-Quality", seen_rows=seen); self.assertEqual(q["primary"]["gen"], 48.3)
    def test_rejects(self):
        self.assertIsNone(run("datalab-to_surya-ocr-2-gguf")["primary"])
        self.assertIn("仅句子抽取", run("DavidAU_LFM2.5-8B-A1B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF")["flags"])
    def test_misc(self):
        self.assertEqual(run("mlx-community_Qwen3.5-27B-Claude-4.6-Opus-Distilled-MLX-4bit")["primary"]["prefill"], 86.5)
        self.assertEqual(run("Jackrong_Qwopus3.8-27B-Flash-V2-GGUF")["primary"]["gen"], 99.0)
        self.assertEqual(run("Youssofal_Ternary-Bonsai-2-27B-MTPLX-Optimized-Speed")["primary"]["gen"], 64.4)
        self.assertIn(39.7, [r["gen"] for r in run("alesha-pro_Qwen3.8-27B-S-mirai-GGUF")["rows"]])
        self.assertEqual(run("peculiar-ragdoll_Cyber-Tiel-Coder-35B-A3B-GGUF-MTP")["primary"]["gen"], 78.2)
if __name__ == "__main__": unittest.main()
