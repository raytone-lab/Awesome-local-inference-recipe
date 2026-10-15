import os, re, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import normalize_engines as N, tag_recipes as T


class EngineRuleOrder(unittest.TestCase):
    def test_every_canonical_engine_name_maps_to_itself(self):
        for _, canonical in N.RULES:
            if canonical is not None:
                self.assertEqual(N.canon(canonical), canonical, f'an earlier rule shadows {canonical!r}')

    def test_strata_mlx_is_not_swallowed_by_strata(self):
        self.assertEqual(N.canon('strata-mlx 0.4.1'), 'strata-mlx')
        self.assertEqual(N.canon('STRATA-MLX'), 'strata-mlx')
        self.assertEqual(N.canon('Strata v0.1.42'), 'Strata')

    def test_canonical_fork_names_are_kept_verbatim(self):
        self.assertEqual(N.canon('llama.cpp (Radiance fork)'), 'llama.cpp (Radiance fork)')


class FamilyRuleOrder(unittest.TestCase):
    def test_specific_families_win_over_generic_ones(self):
        for model, family in [('Qwen-Image 2.1', 'Qwen-Image'), ('Qwen-Image-Edit', 'Qwen-Image'), ('Qwen3.8-27B', 'Qwen'),
                              ('FastH3 V2', 'MiniMax H3'), ('MiniMax H3', 'MiniMax H3'), ('Z-Image Turbo', 'Z-Image')]:
            self.assertEqual(T.family(model), family, model)

    def test_every_family_name_maps_to_itself(self):
        for pattern, family in T.FAMILIES:
            if not re.search(pattern, family, re.I):
                continue
            self.assertEqual(T.family(family), family, f'an earlier rule shadows {family!r}')

    def test_wan_requires_version(self):
        self.assertEqual(T.family('Wan2.2'), 'Wan')


if __name__ == '__main__': unittest.main()
