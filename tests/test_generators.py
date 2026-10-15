import re, sys, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
import gen_readme, gen_site, gen_recipe_pages
from dataset_constants import BUDGET_TIER_BOUNDS_USD


class EnglishFilter(unittest.TestCase):
    def test_readme_treats_curly_quotes_as_cjk(self):
        self.assertEqual(gen_readme.en('Mac Studio “M4 128G”（帖文原话）'), 'Mac Studio')

    def test_site_keeps_curly_quoted_latin_words(self):
        self.assertEqual(gen_site.en('Mac Studio “M4 128G”（帖文原话）'), 'Mac Studio “M4 128G”')

    def test_site_splits_full_width_separators_before_filtering(self):
        self.assertEqual(gen_site.normalize_punct('a；b，c'), 'a; b, c')
        self.assertEqual(gen_site.en('RTX 4090；单卡'), 'RTX 4090')

    def test_site_falls_back_to_original_when_nothing_is_left(self):
        self.assertEqual(gen_site.en('二手显卡'), '二手显卡')

    def test_recipe_pages_returns_none_when_nothing_is_left(self):
        self.assertIsNone(gen_recipe_pages.en('二手显卡'))
        self.assertIsNone(gen_recipe_pages.en(''))


class BudgetTiers(unittest.TestCase):
    def test_every_language_has_one_label_per_bound(self):
        for lang, t in gen_readme.L.items():
            self.assertEqual(len(t['tiers']), len(BUDGET_TIER_BOUNDS_USD), lang)
            self.assertEqual(len(t['tdesc']), len(BUDGET_TIER_BOUNDS_USD), lang)

    def test_english_labels_name_their_bounds(self):
        for label, (lo, hi) in zip(gen_readme.L['en']['tiers'], BUDGET_TIER_BOUNDS_USD):
            self.assertIn(f'{hi/1000:g}k', label)
            if lo: self.assertIn(f'${lo/1000:g}k', label)


class QuickAnswerHardware(unittest.TestCase):
    def test_patterns_reject_multi_device_setups(self):
        for key, rx in gen_readme.QA_SINGLE_DEVICE_HW:
            if key in ('m3u', 'strix'): continue
            self.assertIsNone(re.search(rx, '2× RTX 3090'), key)
            self.assertIsNone(re.search(rx, '2× DGX Spark'), key)


class HardwarePages(unittest.TestCase):
    def test_explorer_query_finds_rows_the_page_lists(self):
        for page in gen_site.HW:
            matched = [r['hardware'] for r in gen_site.D if re.search(page.pattern, r['hardware'])]
            if matched:
                self.assertTrue(any(page.explorer_query in hw for hw in matched), page.slug)


if __name__ == '__main__': unittest.main()
