"""Hafıza katmanı birim testleri: geçici veritabanıyla arşiv + önbellek."""
import os
import tempfile
import unittest

from src import config
from src.services import memory

DETAILS = {"tmdb_id": 42, "media_type": "movie", "title": "Test Film", "year": "2020"}
ANALYSIS = {"bulgular": ["bulgu 1"], "kadin_karakterler": [{"isim": "Ayşe"}]}


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._old_db = config.DB_PATH
        config.DB_PATH = os.path.join(self._tmp.name, "test.db")

    def tearDown(self):
        config.DB_PATH = self._old_db
        self._tmp.cleanup()

    def test_cache_miss_then_hit(self):
        self.assertIsNone(memory.get_cached("movie", 42))
        memory.save_analysis(DETAILS, "# rapor", ANALYSIS)
        cached = memory.get_cached("movie", 42)
        self.assertIsNotNone(cached)
        self.assertEqual(cached["report_md"], "# rapor")

    def test_save_is_idempotent_per_title(self):
        memory.save_analysis(DETAILS, "# eski", ANALYSIS)
        memory.save_analysis(DETAILS, "# yeni", ANALYSIS)
        self.assertEqual(len(memory.list_analyses()), 1)
        self.assertEqual(memory.get_cached("movie", 42)["report_md"], "# yeni")

    def test_list_and_get(self):
        memory.save_analysis(DETAILS, "# rapor", ANALYSIS)
        rows = memory.list_analyses()
        self.assertEqual(rows[0]["title"], "Test Film")
        full = memory.get_analysis(rows[0]["id"])
        self.assertIn("bulgu 1", full["analysis_json"])


if __name__ == "__main__":
    unittest.main()
