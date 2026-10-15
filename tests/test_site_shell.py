"""The site header is copied into each HTML page (no build step); keep the copies identical."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "explore.html", "speed.html", "submit.html"]
HEADER = re.compile(r'<header class="site-hd">.*?</header>', re.S)


def header(page):
    m = HEADER.search((ROOT / page).read_text(encoding="utf-8"))
    return m.group(0) if m else None


class TestSiteShell(unittest.TestCase):
    def test_each_page_has_header(self):
        for p in PAGES:
            with self.subTest(page=p):
                self.assertIsNotNone(header(p))

    def test_active_link_points_at_own_page(self):
        for p in PAGES:
            with self.subTest(page=p):
                active = re.findall(r'<a href="([^"]+)"[^>]*aria-current="page"', header(p))
                self.assertEqual(active, [p])

    def test_header_identical_across_pages(self):
        norm = {p: header(p).replace(' aria-current="page"', "") for p in PAGES}
        ref = norm[PAGES[0]]
        for p in PAGES[1:]:
            with self.subTest(page=p):
                self.assertEqual(norm[p], ref)


if __name__ == "__main__":
    unittest.main()
