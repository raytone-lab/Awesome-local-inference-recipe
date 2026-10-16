import json, re, subprocess, unittest
from collections import defaultdict
from pathlib import Path
R = Path(__file__).resolve().parent.parent

def node(expr):
    js = "global.window=global;require('./cost.js');const D=require('./data/recipes.json');process.stdout.write(JSON.stringify(" + expr + "))"
    return json.loads(subprocess.run(['node', '-e', js], cwd=R, capture_output=True, text=True, check=True).stdout)

def measured_text(D):
    return [r for r in D if r['category'] == 'text' and r['source_level'] == '实测' and r['tok_s'] and '自称' not in (r['metric'] or '') and not r.get('superseded_by')]

class SiteTruth(unittest.TestCase):
    def setUp(self):
        self.D = json.loads((R/'data/recipes.json').read_text(encoding='utf-8'))

    def test_hot_cards_one_per_post_and_never_claimed(self):
        ids = node('hotPosts(D,6).map(r=>r.id)')
        by = {r['id']: r for r in self.D}
        self.assertEqual(len(ids), 6)
        self.assertEqual(len({by[i]['source_url'] for i in ids}), 6)
        self.assertTrue(all(by[i]['source_level'] != '宣称' for i in ids))

    def test_every_x_post_has_as_of_date(self):
        for r in self.D:
            if r.get('x_post'): self.assertRegex(r['x_post'].get('as_of', ''), r'^\d{4}-\d{2}-\d{2}$', r['id'])

    def test_tagline_speedup_is_backed_by_same_hardware_same_model_rows(self):
        h1 = re.search(r'<h1 data-i18n="h1">(.*?)</h1>', (R/'index.html').read_text(encoding='utf-8')).group(1)
        claim = float(re.search(r'([\d.]+)×', h1).group(1))
        g = defaultdict(list)
        for r in measured_text(self.D): g[(r['hardware'], r['model'])].append(r['tok_s'])
        best = max(max(v)/min(v) for v in g.values() if len(v) > 1)
        self.assertGreaterEqual(best, claim, f'tagline claims {claim}×, data backs {best:.2f}×')
        js = (R/'landing.js').read_text(encoding='utf-8')
        self.assertNotRegex(js + h1, r'10×|10 倍')

    def test_json_ld_languages_match_site_languages(self):
        s = (R/'index.html').read_text(encoding='utf-8')
        ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
        langs = {'en'} | {p.name for p in (R/'guides').iterdir() if p.is_dir()}
        self.assertEqual(set(ld['inLanguage']), langs)

    def test_home_rankings_use_only_measured_rows(self):
        ids = node("D.filter(r=>r.category=='text'&&r.source_level=='实测'&&!selfReported(r)&&r.tok_s&&r.hardware_cost_usd&&!r.superseded_by).map(r=>r.id)")
        self.assertNotIn('text-113', ids)
        self.assertIn("r.source_level==MEA&&!selfReported(r)", (R/'landing.js').read_text(encoding='utf-8'))

if __name__ == '__main__': unittest.main()
