import json, sys, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R/'scripts'))
import gen_watchlist

class Watchlist(unittest.TestCase):
    def setUp(self):
        self.src = json.loads((R/'data/sources.json').read_text(encoding='utf-8'))
        self.md = (R/'docs/watchlist.md').read_text(encoding='utf-8')
    def test_file_matches_generator(self):
        self.assertEqual(self.md, gen_watchlist.render(self.src))
    def test_every_source_has_one_row(self):
        rows = [l for l in self.md.splitlines() if l.startswith('| ') and '](' in l]
        self.assertEqual(len(rows), len(self.src['sources']))
        for s in self.src['sources']:
            self.assertIn(f"]({s['url']})", self.md, s['name'])
    def test_rows_sorted_by_tier_and_pipes_escaped(self):
        out = gen_watchlist.render({'updated': '2026-01-01', 'sources': [
            {'tier': 'C', 'name': 'c', 'url': 'u1', 'platform': 'X', 'followers': None, 'focus': 'a|b', 'why': 'w', 'sample_post': 's'},
            {'tier': 'A', 'name': 'a', 'url': 'u2', 'platform': 'Web', 'followers': 5, 'focus': 'f', 'why': 'w', 'sample_post': 's'}]})
        rows = [l for l in out.splitlines() if l.startswith('| ') and '](' in l]
        self.assertTrue(rows[0].startswith('| A |')); self.assertIn('a\\|b', rows[1]); self.assertIn('| — |', rows[1])

if __name__ == '__main__': unittest.main()
