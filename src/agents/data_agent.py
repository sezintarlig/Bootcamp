"""Veri Agent: TMDb'den yapımı doğrular ve analiz bağlamını hazırlar.

Bu agent LLM kullanmaz; pipeline'ın deterministik ilk halkasıdır. Görevleri:
yapım detayını çekmek, karakter listesini normalize etmek ve sonraki
agent'ların kullanacağı metin bağlamını üretmek.
"""
from src.services import tmdb


class DataAgent:
    name = "Veri Agent"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def run(self, media_type: str, tmdb_id: int) -> dict:
        details = tmdb.get_details(media_type, tmdb_id, self.api_key)
        details["context_text"] = self._build_context(details)
        return details

    @staticmethod
    def _build_context(d: dict) -> str:
        kind = "Film" if d["media_type"] == "movie" else "Dizi"
        cast_lines = "\n".join(
            f"- {c['character']} (oynayan: {c['name']}, oyuncu cinsiyeti: {c['gender']})"
            for c in d["cast"]
        )
        return (
            f"{kind}: {d['title']} ({d['year']})\n"
            f"Türler: {', '.join(d['genres']) or 'belirtilmemiş'}\n"
            f"Özet (TMDb): {d['overview'] or 'yok'}\n"
            f"Başlıca karakterler:\n{cast_lines or '- karakter verisi yok'}"
        )
