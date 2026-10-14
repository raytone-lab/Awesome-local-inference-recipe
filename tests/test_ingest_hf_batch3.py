"""2026-10-14 v3 批次 12 张卡的回归测试（金标准为人工审核结果）"""
import os, sys, unittest
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "scripts"))
from hf_extract import extract
def run(n, **k):
    with open(os.path.join(H, "fixtures", "hf", n + ".md")) as f: return extract(n.replace("_", "/", 1), f.read(), **k)
def gens(e, hw=None): return [r["gen"] for r in e["rows"] if hw is None or (r["hardware"] and hw.lower() in r["hardware"].lower())]

class Batch3(unittest.TestCase):
    def test_comparator_cols_and_mean_row(self):
        e = run("umixer_Qwen3.8-Flash-Next-oQ4e-mix6-mtp")
        self.assertEqual((e["primary"]["gen"], e["primary"]["prefill"]), (84.4, 2377.1))
        self.assertNotIn(73.6, gens(e)); self.assertNotIn(75.7, gens(e))
    def test_bpw_quant_and_all_rows(self):
        e = run("byteshape_Qwen3.8-27B-GGUF")
        self.assertEqual(e["primary"]["quant"], "GPU-1 (2.56 bpw)")
        for v in (119, 111, 108, 104, 94, 176, 167): self.assertIn(v, gens(e))
        self.assertTrue(all("GPU" not in (r["hardware"] or "") for r in e["rows"]))
    def test_headline_is_peak_and_prose_cell(self):
        e = run("agentionai_Qwen3.8-Flash-Next-Gyro-GGUF")
        self.assertNotEqual(e["primary"]["gen"], 221); self.assertFalse(e["primary"]["peak_claim"])
        self.assertTrue(all(r["peak_claim"] for r in e["rows"] if r["gen"] in (221, 218)))
        self.assertIn(140, gens(e, "5090"))
    def test_workstation_and_radeon_hw(self):
        e = run("agentionai_Qwen3.8-Flash-Next-Gyro-GGUF")
        a6 = [r for r in e["rows"] if r["gen"] == 57.4][0]; self.assertIn("A6000", a6["hardware"]); self.assertTrue(a6["excluded"])
        self.assertEqual(gens(e, "R9700"), [57.8]); self.assertIsNone([r for r in e["rows"] if r["gen"] == 114][0]["prefill"])
    def test_noise_metrics_dropped(self):
        self.assertIsNone(run("mlx-community_CLM-v0.1-8B-MLX-8bit")["primary"])
        self.assertIsNone(run("mlx-community_clef-omni-4bit")["primary"])
    def test_foreign_link_sentence(self):
        e = run("tfwnotops_Ternary-Bonsai-2-27B-ConstantKV")
        self.assertNotIn(470, gens(e)); self.assertIn("Mac mini", e["primary"]["hardware"])
    def test_sentence_cards_unchanged(self):
        self.assertEqual(run("AtomicChat_Qwen3.8-Flash-Next-GGUF")["primary"]["gen"], 36)
        self.assertEqual(run("ddalcu_Qwen3.8-Flash-Next-MLX-Serve-iQ-MLX-4.7bpw")["primary"]["gen"], 157)
        self.assertEqual(run("Youssofal_Qwen3.6-27B-MTPLX-Optimized-Speed")["primary"]["gen"], 63.056)
        self.assertEqual(run("OsaurusAI_Allosaurus-v0.1-125B-A6B-JANGH2")["primary"]["gen"], 46.5)
if __name__ == "__main__": unittest.main()
