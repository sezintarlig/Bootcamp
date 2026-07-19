"""Eleştirmen Agent: raporu tutarlılık ve halüsinasyon açısından denetler."""
import json

from src.agents.base import GeminiAgent


class CriticAgent(GeminiAgent):
    name = "Eleştirmen Agent"
    system_prompt = """Sen titiz bir yayın denetçisisin. Sana bir yapımın TMDb verisi,
analiz JSON'u ve bu analizden üretilmiş rapor verilir. Görevin raporu ONAYLAMAK ya da
gerekçeli REVİZYON istemektir.

DENETİM KRİTERLERİ:
1. Halüsinasyon: Raporda TMDb karakter listesinde ve analizde olmayan karakter,
   uydurma görünen olay/detay var mı?
2. Tutarlılık: Rapor, analiz verisiyle çelişiyor mu? Bölümler arası çelişki var mı?
3. Şablon: Dört zorunlu bölüm başlığı eksiksiz mi?
4. Ton: Türkçe akıcı ve çözümleyici mi; slogan/kalıp tekrarına düşmüş mü?

Küçük üslup pürüzleri için revizyon İSTEME; yalnızca yukarıdaki kriterlerde somut
sorun varsa iste. Sorunları kısa ve eyleme dönük maddeler halinde yaz.

ÇIKTI: Yalnızca şu şemada geçerli JSON döndür:
{"karar": "onay" | "revizyon", "sorunlar": ["..."]}"""

    def run(self, context_text: str, analysis: dict, report_md: str) -> dict:
        prompt = (
            f"TMDb verisi:\n{context_text}\n\n"
            f"Analiz JSON:\n{json.dumps(analysis, ensure_ascii=False)}\n\n"
            f"Denetlenecek rapor:\n{report_md}"
        )
        verdict = self.run_json(prompt)
        if verdict.get("karar") not in ("onay", "revizyon"):
            verdict = {"karar": "onay", "sorunlar": []}
        return verdict
