"""TMDb servisi: yapım arama, doğrulama ve karakter listesi çıkarma."""
from __future__ import annotations

import requests

BASE_URL = "https://api.themoviedb.org/3"
POSTER_URL = "https://image.tmdb.org/t/p/w185"

# TMDb gender kodları
_GENDER = {0: "bilinmiyor", 1: "kadın", 2: "erkek", 3: "non-binary"}

MAX_CAST = 15


class TMDbError(Exception):
    pass


def _get(path: str, api_key: str, **params) -> dict:
    params = {"api_key": api_key, "language": "tr-TR", **params}
    try:
        resp = requests.get(f"{BASE_URL}{path}", params=params, timeout=15)
    except requests.RequestException as exc:
        raise TMDbError(f"TMDb'ye ulaşılamadı: {exc}") from exc
    if resp.status_code == 401:
        raise TMDbError("TMDb API anahtarı geçersiz.")
    if not resp.ok:
        raise TMDbError(f"TMDb hatası: HTTP {resp.status_code}")
    return resp.json()


def search(query: str, api_key: str) -> list[dict]:
    """Film + dizi araması. Kullanıcıya seçtirmeye uygun sade sonuç listesi döner."""
    data = _get("/search/multi", api_key, query=query, include_adult="false")
    results = []
    for item in data.get("results", []):
        if item.get("media_type") not in ("movie", "tv"):
            continue
        date = item.get("release_date") or item.get("first_air_date") or ""
        results.append(
            {
                "tmdb_id": item["id"],
                "media_type": item["media_type"],
                "title": item.get("title") or item.get("name"),
                "year": date[:4] or "?",
                "overview": item.get("overview") or "",
                "poster_url": POSTER_URL + item["poster_path"] if item.get("poster_path") else None,
            }
        )
    return results[:8]


def get_details(media_type: str, tmdb_id: int, api_key: str) -> dict:
    """Yapım detayı + oyuncu/karakter listesi (analiz bağlamının hammaddesi)."""
    if media_type == "movie":
        data = _get(f"/movie/{tmdb_id}", api_key, append_to_response="credits")
        title = data.get("title")
        year = (data.get("release_date") or "")[:4]
        raw_cast = data.get("credits", {}).get("cast", [])
        cast = [
            {
                "name": c.get("name"),
                "character": c.get("character") or "?",
                "gender": _GENDER.get(c.get("gender", 0), "bilinmiyor"),
            }
            for c in raw_cast[:MAX_CAST]
        ]
    elif media_type == "tv":
        data = _get(f"/tv/{tmdb_id}", api_key, append_to_response="aggregate_credits")
        title = data.get("name")
        year = (data.get("first_air_date") or "")[:4]
        raw_cast = data.get("aggregate_credits", {}).get("cast", [])
        cast = [
            {
                "name": c.get("name"),
                "character": (c.get("roles") or [{}])[0].get("character") or "?",
                "gender": _GENDER.get(c.get("gender", 0), "bilinmiyor"),
            }
            for c in raw_cast[:MAX_CAST]
        ]
    else:
        raise TMDbError(f"Desteklenmeyen tür: {media_type}")

    return {
        "tmdb_id": tmdb_id,
        "media_type": media_type,
        "title": title,
        "year": year,
        "overview": data.get("overview") or "",
        "genres": [g["name"] for g in data.get("genres", [])],
        "cast": cast,
    }
