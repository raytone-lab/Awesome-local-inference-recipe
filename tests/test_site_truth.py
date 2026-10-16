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
        self.assertNotRegex(js + h1, r'10×|10 ?倍|十倍|ten times')

    def test_json_ld_languages_match_site_languages(self):
        s = (R/'index.html').read_text(encoding='utf-8')
        ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
        langs = {'en'} | {p.name for p in (R/'guides').iterdir() if p.is_dir()}
        self.assertEqual(set(ld['inLanguage']), langs)

    def test_home_rankings_use_only_measured_rows(self):
        ids = node("D.filter(r=>r.category=='text'&&r.source_level=='实测'&&!selfReported(r)&&r.tok_s&&r.hardware_cost_usd&&!r.superseded_by).map(r=>r.id)")
        self.assertNotIn('text-113', ids)
        self.assertIn("r.source_level==MEA&&!selfReported(r)", (R/'landing.js').read_text(encoding='utf-8'))

class UpdateXMetrics(unittest.TestCase):
    def setUp(self):
        import sys; sys.path.insert(0, str(R/'scripts')); import update_x_metrics as u; self.u = u
    def test_apply_posts_sets_counts_and_as_of(self):
        recs = [{'source_url': 'https://x.com/a/status/123', 'x_post': {'author': 'a', 'likes': 1, 'reposts': 0}}, {'source_url': 'https://x.com/b/status/9', 'x_post': {'author': 'b', 'likes': 5, 'reposts': 5}}]
        n = self.u.apply_posts(recs, [{'id': '123', 'public_metrics': {'like_count': 40, 'repost_count': 3}}], '2026-10-16')
        self.assertEqual(n, 1)
        self.assertEqual(recs[0]['x_post'], {'author': 'a', 'likes': 40, 'reposts': 3, 'as_of': '2026-10-16'})
        self.assertNotIn('as_of', recs[1]['x_post'])
    def test_apply_users_and_watchlist(self):
        src = {'updated': 'x', 'note': 'Follower counts from X API on 2026-10-14 for X accounts', 'sources': [{'url': 'https://x.com/Mia', 'followers': 1}, {'url': 'https://www.reddit.com/r/x/', 'followers': None}]}
        self.assertEqual(self.u.apply_users(src, [{'username': 'mia', 'public_metrics': {'followers_count': 77}}], '2026-10-16'), 1)
        self.assertEqual((src['sources'][0]['followers'], src['updated'], src['followers_as_of']), (77, '2026-10-16', '2026-10-16'))
        self.assertIn('2026-10-16', src['note'])
        md = 'Generated from `data/sources.json` (2026-10-14). x\n| A | [Mia](https://x.com/Mia) | X | 1 | f |'
        out = self.u.render_watchlist(md, src, '2026-10-16')
        self.assertIn('(2026-10-16)', out); self.assertIn('| X | 77 |', out)

if __name__ == '__main__': unittest.main()
