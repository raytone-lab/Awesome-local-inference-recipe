import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import normalize_engines as N, tag_recipes as T
def rec(**k):
    b = dict(id='t-1', category='text', model='X', quant=None, engine='llama.cpp', hardware='RTX 4090',
             context=None, metric=None, source_url='u1')
    b.update(k); return b
class TestForkAndTags(unittest.TestCase):
    def test_fork_names_kept(self):
        for raw, c in [('llama.cpp (vahpetr fork)', 'llama.cpp (vahpetr fork)'),
                       ('llama.cpp s1-fork + MTP', 'llama.cpp (vahpetr fork)'),
                       ('llama.cpp-omni + LES', 'llama.cpp (OpenBMB fork)'),
                       ('llama.cpp (PrismML fork)', 'llama.cpp (PrismML fork)')]:
            self.assertEqual(N.canon(raw), c, raw)
    def test_no_draft_is_not_speculative(self):
        self.assertNotIn('speculative', T.tags(rec(metric='68 tok/s（无草稿模型）')))
        self.assertNotIn('speculative', T.tags(rec(quant='oMLX（无 MTP/DFlash）')))
        self.assertIn('speculative', T.tags(rec(metric='MTP 头 50 tok/s（无草稿 39）')))
    def test_offload_from_hardware_and_metric(self):
        self.assertIn('offload', T.tags(rec(hardware='RTX 5090 32GB + 系统内存（部分卸载）')))
        self.assertIn('offload', T.tags(rec(metric='超过一半模型从 NVMe 流式读取')))
        self.assertNotIn('offload', T.tags(rec(metric='29 tok/s（SSD 前缀缓存 ~85%）')))
if __name__ == '__main__': unittest.main()
