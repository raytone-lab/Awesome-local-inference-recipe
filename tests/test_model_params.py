import warnings, json, re, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
class ModelParams(unittest.TestCase):
    def setUp(self):
        self.P = json.loads((R / 'data/model-params.json').read_text())['models']
        self.D = json.loads((R / 'data/recipes.json').read_text())
    def match(self, model):
        for m in self.P:
            if re.search(m['match'], model):
                return None if m.get('exclude') and re.search(m['exclude'], model) else m
    def test_fields(self):
        for m in self.P:
            self.assertIn(m['arch'], ('dense', 'moe'), m['label'])
            self.assertTrue(m['source'].startswith('https://huggingface.co/'), m['label'])
            self.assertGreater(m['total_b'], 0); self.assertGreater(m['active_b'], 0)
            self.assertLessEqual(m['active_b'], m['total_b'], m['label'])
            if m['arch'] == 'dense': self.assertEqual(m['active_b'], m['total_b'], m['label'])
            self.assertIn(m.get('quant_native'), (None, 'ternary', '1bit'), m['label'])
            re.compile(m['match']); m.get('exclude') and re.compile(m['exclude'])
    def test_known_traps(self):
        self.assertIsNone(self.match('Bonsai 27B 1-bit'))
        self.assertIsNone(self.match('DeepSeek-V4.1-Flash（REAP 256 专家剪枝）'))
        self.assertEqual(self.match('Bonsai2 27B')['label'], 'Bonsai 2 27B')
        self.assertEqual(self.match('DeepSeek-V4-Flash (0731)')['label'], 'DeepSeek-V4-Flash')
    def test_hero_rows_covered_or_listed(self):
        # every measured priced text row either maps to a card or is knowingly excluded
        miss = sorted({r['model'] for r in self.D if r['category'] == 'text' and r['tok_s'] and r['hardware_cost_usd']
                       and r['source_level'] == '实测' and not self.match(r['model'])})
        # warning, not failure: new data PRs may add models before a card exists (they are just left off the hero)
        miss = [m for m in miss if not re.search(r'REAP', m)]
        if miss: warnings.warn(f'models missing from data/model-params.json (omitted from hero): {miss}')
    def test_every_hero_group_nonempty_for_known_models(self):
        # hard check that the card regexes still match the headline models
        for name in ('Qwen3.8-27B', 'Qwen3.8-Flash-Next', 'LFM2.5-24B-A2B'):
            self.assertIsNotNone(self.match(name), name)
if __name__ == '__main__': unittest.main()
