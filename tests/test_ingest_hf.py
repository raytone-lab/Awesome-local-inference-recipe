import os, sys, unittest
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "scripts"))
from hf_extract import extract
def F(n):
    with open(os.path.join(H, "fixtures", "hf", n + ".md")) as f: return f.read()
def run(n, **k): return extract(n.replace("_", "/", 1), F(n), **k)
def find(res, hw, quant=None):
    return [r for r in res["rows"] if r["hardware"] and hw.lower() in r["hardware"].lower() and (quant is None or (r["quant"] or "").upper() == quant.upper())]

class T(unittest.TestCase):
    def test_cdiamond(self):
        r = run("cdiamond_Qwen3.8-27B-iMatrix-NVFP4-MTP-GGUF", include_nonconsumer=True)
        self.assertEqual(r["primary"]["gen"], 50.441)
        self.assertNotIn(815.64, [x["gen"] for x in r["rows"]])
        self.assertIn(12.606, [x["gen"] for x in r["rows"]]); self.assertIn(226.75, [x["prefill"] for x in r["rows"]])
        self.assertIn("RTX PRO 4000", r["primary"]["hardware"]); self.assertEqual(r["primary"]["hw_class"], "workstation")
        self.assertEqual(r["context_tokens"], 262144)
        self.assertTrue(any("separate" in c for c in r["caveats"]))
        d = run("cdiamond_Qwen3.8-27B-iMatrix-NVFP4-MTP-GGUF"); self.assertIsNone(d["primary"], "workstation cards are excluded by default")
    def test_bonsai2_gguf(self):
        r = run("prism-ml_Ternary-Bonsai-2-27B-gguf")
        g = {(x["hardware"], x["quant"]): (x["gen"], x["prefill"]) for x in r["rows"] if not x["excluded"]}
        self.assertEqual(find(r, "RTX 5090", "PQ2_0")[0]["gen"], 129.9); self.assertEqual(find(r, "RTX 5090", "PQ2_0")[0]["prefill"], 3893)
        self.assertEqual(find(r, "RTX 5090", "PTQ1_0")[0]["gen"], 120.5)
        self.assertEqual(find(r, "RTX 4090", "PTQ1_0")[0]["gen"], 91.1)
        self.assertEqual(find(r, "M4 Pro")[0]["gen"], 18.0); self.assertEqual(find(r, "M5 Max")[0]["prefill"], 765)
        self.assertTrue(all(x["excluded"] for x in find(r, "H100") + find(r, "A100") + find(r, "L4")))
        self.assertTrue(find(r, "RTX PRO 6000")[0]["excluded"])
        self.assertTrue(any("pending" in c.lower() for c in r["caveats"]))
    def test_bonsai_dup(self):
        a = run("prism-ml_Ternary-Bonsai-2-27B-gguf"); b = run("prism-ml_Ternary-Bonsai-2-27B-mlx-2bit")
        self.assertEqual(a["table_fingerprint"], b["table_fingerprint"])
    def test_bonsai_1bit(self):
        r = run("prism-ml_Bonsai-27B-mlx-1bit")
        self.assertEqual(find(r, "M5 Max")[0]["gen"], 66.4); self.assertEqual(find(r, "iPhone")[0]["gen"], 11.0)
        self.assertEqual(find(r, "M4 Pro")[0]["prefill"], 133)
        self.assertTrue(find(r, "H100")[0]["excluded"])
    def test_ista(self):
        r = run("ISTA-DASLab_Qwen3.8-Flash-Next-GSQ-RCO-GGUF")
        q = {x["quant"]: x for x in r["rows"]}
        self.assertEqual((q["Q2_0"]["gen"], q["Q2_0"]["prefill"]), (93.79, 367.49))
        self.assertEqual((q["IQ2_XS"]["gen"], q["IQ2_XS"]["prefill"]), (70.30, 108.19))
        self.assertIsNone(q["Q2_0"]["hardware"])
    def test_tiel(self):
        r = run("peculiar-ragdoll_Tiel-Coder-35B-A3B-GGUF-MTP")
        gens = [x["gen"] for x in r["rows"]]
        self.assertEqual(gens[:2], [77.4, 94.4]); self.assertIsNone(r["primary"]["hardware"])
        self.assertTrue(any("our box" in c for c in r["caveats"]))
    def test_humanlike_datacenter(self):
        r = run("LessThanThreeAI_Qwen3.8-27B-Humanlike-Chat-GGUF")
        self.assertIn("H100", " ".join(r["declared_hardware"]))
        self.assertTrue(all(x["excluded"] for x in r["rows"] if x["hardware"] and "H100" in x["hardware"]))
    def test_low_conf(self):
        self.assertIn("<3B 小模型", run("harshatheg_Qwen-2.5-1B-RLCD")["flags"])
        self.assertIn("含占位链接", run("harshatheg_Qwen-2.5-1B-RLCD")["flags"])
        o = run("FluidInference_unlimited-ocr-mlx-coreml"); self.assertTrue(any("OCR" in f for f in o["flags"])); self.assertLess(o["confidence"], 0.5)
if __name__ == "__main__": unittest.main()
