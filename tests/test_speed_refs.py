"""speed.html reference data must point at real recipes and quote numbers that appear in them."""
import json, re, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent

class SpeedRefs(unittest.TestCase):
    def test_prefill_presets_are_measured_and_quoted(self):
        refs = json.loads((R / 'data/speed-refs.json').read_text())
        rec = {r['id']: r for r in json.loads((R / 'data/recipes.json').read_text())}
        for it in refs['prefill']['items'] + [{'id': i} for i in refs['mtp']['ids']]:
            r = rec.get(it['id']); self.assertIsNotNone(r, it['id'])
            self.assertEqual(r['source_level'], '实测', it['id'])
            if 'pp' in it:
                note = (r.get('source_note', '') + ' ' + r.get('metric', '')).replace(',', '')
                self.assertRegex(note, rf'(?<!\d){it["pp"]}(?!\d)', it['id'])
            if 'check' in it:
                self.assertIn(it['check'], r.get('source_note', '') + ' ' + r.get('metric', ''))

    def test_token_stats_present(self):
        tk = json.loads((R / 'data/speed-tokens.json').read_text())
        for lang in ('en', 'zh-CN', 'ja'):
            self.assertEqual(tk['stats'][lang]['tokens'], len(tk['texts'][lang]))

if __name__ == '__main__':
    unittest.main()
