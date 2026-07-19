"""Özet kart üretici birim testleri."""
import unittest

from src.services.card import generate_card

ANALYSIS = {
    "kadin_temsili_yok": False,
    "kadin_karakterler": [{"isim": "Nihal"}, {"isim": "Necla"}],
    "bulgular": ["Entelektüel ataerki eleştirisi", "Ekonomik bağımlılık", "Dayanışma eksikliği"],
}


class CardTests(unittest.TestCase):
    def test_returns_png_bytes(self):
        png = generate_card("Kış Uykusu", "2014", "movie", ANALYSIS)
        self.assertTrue(png.startswith(b"\x89PNG"))
        self.assertGreater(len(png), 5000)

    def test_no_representation_variant(self):
        analysis = {"kadin_temsili_yok": True, "kadin_karakterler": [], "bulgular": ["Mutlak yokluk"]}
        png = generate_card("Arabistanlı Lawrence", "1962", "movie", analysis)
        self.assertTrue(png.startswith(b"\x89PNG"))

    def test_long_title_and_findings_fit(self):
        analysis = dict(ANALYSIS, bulgular=["Ç" * 400, "b" * 300, "c" * 300])
        png = generate_card("Çok Uzun Bir Film Adı " * 4, "2021", "tv", analysis)
        self.assertTrue(png.startswith(b"\x89PNG"))


if __name__ == "__main__":
    unittest.main()
