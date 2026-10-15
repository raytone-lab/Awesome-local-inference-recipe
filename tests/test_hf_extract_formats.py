import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from hf_extract import extract, is_comparator


def rows(card):
    return [(r["hardware"], r["gen"], r["prefill"], r["quant"]) for r in extract("org/Model-27B", card)["rows"]]


class SentenceFormats(unittest.TestCase):
    def test_speed_followed_by_on_hardware(self):
        self.assertEqual(rows("Runs at 44 tok/s on an M5 Pro."), [("M5 Pro", 44.0, None, None)])

    def test_list_items_are_separate_sentences(self):
        card = "Speeds:\n- 30 tok/s on RTX 4090\n- 50 tok/s on RTX 5090\n"
        self.assertEqual(rows(card), [("RTX 4090", 30.0, None, None), ("RTX 5090", 50.0, None, None)])

    def test_sentence_linking_another_model_is_dropped(self):
        self.assertEqual(rows("The base https://huggingface.co/other/Base runs 90 tok/s on RTX 4090."), [])


class TableFormats(unittest.TestCase):
    def test_multi_context_table_keeps_only_the_mean_row(self):
        card = "Measured on RTX 4090:\n\n| Context | tg tok/s |\n|---|---|\n| 4k | 50 |\n| 32k | 40 |\n| Mean | 45 |\n"
        self.assertEqual(rows(card), [("RTX 4090", 45.0, None, None)])

    def test_prefixed_prefill_pairs_only_with_same_prefix_decode(self):
        card = ("Measured on RTX 5090:\n\n| Config | Gyro-S prefill | Gyro-S decode | Gyro-M decode |\n|---|---|---|---|\n"
                "| Q4 | 1000 tok/s | 80 tok/s | 60 tok/s |\n")
        self.assertEqual(rows(card), [("RTX 5090", 80.0, 1000.0, "Q4"), ("RTX 5090", 60.0, None, "Q4")])

    def test_paired_column_named_as_card_comparator_is_skipped(self):
        card = "Compared vs uniform oQ4e.\n\nMeasured on M3 Ultra:\n\n| Model | oQ4e tg | oQ3 tg |\n|---|---|---|\n| 27B | 40 | 55 |\n"
        self.assertEqual(rows(card), [("M3 Ultra", 55.0, None, None)])
        self.assertTrue(is_comparator("oQ4e tg", "vs uniform oQ4e"))
        self.assertFalse(is_comparator("oQ3 tg", "vs uniform oQ4e"))

    def test_quant_prefixed_columns_become_one_row_per_quant(self):
        card = "Measured on RTX 4090:\n\n| Model | PQ2_0 TG128 | PTQ1_0 TG128 |\n|---|---|---|\n| 8B | 100 | 150 |\n"
        self.assertEqual(rows(card), [("RTX 4090", 100.0, None, "PQ2_0"), ("RTX 4090", 150.0, None, "PTQ1_0")])


if __name__ == "__main__": unittest.main()
