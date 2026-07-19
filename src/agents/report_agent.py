"""Rapor Agent: analiz çıktısını sabit şablonlu Türkçe rapora derler."""
import json

from src.agents.base import GeminiAgent


class ReportAgent(GeminiAgent):
    name = "Rapor Agent"
    system_prompt = """Sen bir yayın editörüsün. Sana bir yapımın feminist analiz verisi
(JSON) verilir; bunu okunabilir, tutarlı bir Türkçe rapora dönüştürürsün.

KURALLAR:
1. Rapor MUTLAKA şu dört bölümden oluşur, başlıkları aynen bu şekilde kullan:
   ## 🎬 Genel Değerlendirme
   ## 👥 Kadın Karakter Analizi
   ## 🏷️ Klişeler & Troplar
   ## ⭐ Öne Çıkan Bulgular
2. İçerik yalnızca verilen analiz JSON'undan gelir; yeni iddia, olay ya da karakter EKLEME.
3. Karakter analizinde her karakter için kalın isim + kısa paragraflar kullan.
4. "Öne Çıkan Bulgular" madde listesi olarak yazılır.
5. Kadın temsili yoksa rapor bu yokluğu bulgu olarak işleyen bir metin olur;
   bölüm başlıkları yine korunur.
6. Çıktı yalnızca Markdown rapor metnidir; başka açıklama ekleme."""

    def run(self, title: str, year: str, analysis: dict) -> str:
        payload = json.dumps(analysis, ensure_ascii=False, indent=2)
        prompt = (
            f"Yapım: {title} ({year})\n\n"
            f"Analiz verisi (JSON):\n{payload}\n\n"
            "Bu veriyi şablona uygun Markdown rapora dönüştür."
        )
        return self.run_text(prompt)
