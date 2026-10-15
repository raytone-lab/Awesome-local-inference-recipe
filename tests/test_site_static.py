import json, re, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
class SiteStatic(unittest.TestCase):
    def setUp(self):
        self.D = json.loads((R/'data/recipes.json').read_text(encoding='utf-8'))
        self.sm = (R/'sitemap.xml').read_text(encoding='utf-8')
    def test_explore_fallback_has_every_row(self):
        s = (R/'explore.html').read_text(encoding='utf-8')
        block = re.search(r'<!--static:rows.*?<!--/static-->', s, re.S).group(0)
        self.assertEqual(len(re.findall(r'<tr data-id=', block)), len(self.D))
    def test_sitemap_lists_only_indexable_existing_pages(self):
        base = 'https://raytone-lab.github.io/awesome-local-inference-recipes/'
        for u in re.findall(r'<loc>([^<]+)</loc>', self.sm):
            self.assertTrue(u.startswith(base), u)
            rel = u[len(base):] or 'index.html'
            p = R/rel; self.assertTrue(p.exists(), rel)
            self.assertNotIn('noindex', p.read_text(encoding='utf-8'), rel)
        for p in list((R/'hw').glob('*.html')) + list((R/'model').glob('*.html')):
            s = p.read_text(encoding='utf-8'); n = s.count('<tr>') - 1
            self.assertEqual('noindex' in s, n < 5, p.name)
    def test_guides_hreflang_reciprocal_and_self_canonical(self):
        for p in (R/'guides').rglob('*.html'):
            if p.name == 'index.html': continue
            s = p.read_text(encoding='utf-8')
            canon = re.search(r'rel="canonical" href="([^"]+)"', s).group(1)
            alts = dict(re.findall(r'hreflang="([^"]+)" href="([^"]+)"', s))
            self.assertIn(canon, alts.values(), p)
            self.assertIn('x-default', alts)
            self.assertNotIn('HowTo', s); self.assertNotIn('FAQPage', s)
if __name__ == '__main__': unittest.main()
