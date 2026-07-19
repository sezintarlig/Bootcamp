"""Agent altyapısı birim testleri (ağ gerektirmez)."""
import unittest

from src.agents.base import DEFAULT_RETRY_DELAY, _quota_delay


class QuotaDelayTests(unittest.TestCase):
    def test_429_with_suggested_delay(self):
        exc = Exception("429 RESOURCE_EXHAUSTED ... Please retry in 14.6452s.")
        self.assertAlmostEqual(_quota_delay(exc), 15.6452, places=3)

    def test_429_without_delay_uses_default(self):
        exc = Exception("429 RESOURCE_EXHAUSTED: quota exceeded")
        self.assertEqual(_quota_delay(exc), DEFAULT_RETRY_DELAY)

    def test_non_quota_error_returns_none(self):
        self.assertIsNone(_quota_delay(Exception("500 INTERNAL")))
        self.assertIsNone(_quota_delay(Exception("404 NOT_FOUND")))


if __name__ == "__main__":
    unittest.main()
