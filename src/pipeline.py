"""Orkestrasyon: Veri → Feminist Analiz → Rapor → Eleştirmen (max 1 düzeltme turu).

Framework kullanılmaz; akış bu modülde açıkça yönetilir.
"""
from typing import Callable

from google import genai

from src.agents.analysis_agent import AnalysisAgent
from src.agents.critic_agent import CriticAgent
from src.agents.data_agent import DataAgent
from src.agents.report_agent import ReportAgent
from src.config import GEMINI_MODEL

MAX_REVISIONS = 1

HONESTY_MESSAGE = (
    "## 🎬 Genel Değerlendirme\n\n"
    "Bu yapım hakkında güvenilir bir feminist analiz üretecek kadar bilgim yok. "
    "Uydurma bir analiz sunmak yerine bunu açıkça belirtmeyi tercih ediyorum.\n\n"
    "Daha bilinen bir yapım deneyebilir ya da başlığın doğru yapımla eşleştiğinden "
    "emin olabilirsiniz."
)


class Pipeline:
    def __init__(self, tmdb_key: str, gemini_key: str, model: str = GEMINI_MODEL):
        client = genai.Client(api_key=gemini_key)
        self.data_agent = DataAgent(tmdb_key)
        self.analysis_agent = AnalysisAgent(client, model)
        self.report_agent = ReportAgent(client, model)
        self.critic_agent = CriticAgent(client, model)

    def run(
        self,
        media_type: str,
        tmdb_id: int,
        on_step: Callable[[str], None] = lambda msg: None,
    ) -> dict:
        """Analizi uçtan uca çalıştırır; sonuç sözlüğü döndürür."""
        on_step("🔎 Veri Agent: yapım doğrulanıyor, karakter listesi çekiliyor…")
        details = self.data_agent.run(media_type, tmdb_id)

        on_step("🧠 Feminist Analiz Agent: karakterler analiz ediliyor…")
        analysis = self.analysis_agent.run(details["context_text"])

        if analysis.get("tanima_durumu") == "yetersiz":
            on_step("🛑 Dürüstlük koruması devrede: yapım yeterince tanınmıyor.")
            return {
                "details": details,
                "analysis": analysis,
                "report_md": HONESTY_MESSAGE,
                "honest_refusal": True,
                "revised": False,
            }

        on_step("📝 Rapor Agent: rapor derleniyor…")
        report_md = self.report_agent.run(details["title"], details["year"], analysis)

        revised = False
        for _ in range(MAX_REVISIONS):
            on_step("🔍 Eleştirmen Agent: rapor denetleniyor…")
            verdict = self.critic_agent.run(details["context_text"], analysis, report_md)
            if verdict["karar"] == "onay":
                break
            on_step("♻️ Eleştirmen sorun buldu, düzeltme turu çalışıyor…")
            revised = True
            analysis = self.analysis_agent.run(
                details["context_text"], revision_notes=verdict.get("sorunlar", [])
            )
            report_md = self.report_agent.run(details["title"], details["year"], analysis)

        on_step("✅ Analiz tamamlandı.")
        return {
            "details": details,
            "analysis": analysis,
            "report_md": report_md,
            "honest_refusal": False,
            "revised": revised,
        }
