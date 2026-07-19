"""Anahtar ve ayar yönetimi: önce ortam değişkeni (.env), yoksa Streamlit secrets."""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DB_PATH = os.getenv("MEDIA_MIRROR_DB", "media_mirror.db")


def _streamlit_secret(name: str):
    try:
        import streamlit as st

        return st.secrets.get(name)
    except Exception:
        return None


def get_key(name: str) -> str | None:
    return os.getenv(name) or _streamlit_secret(name)


def tmdb_api_key() -> str | None:
    return get_key("TMDB_API_KEY")


def gemini_api_key() -> str | None:
    return get_key("GEMINI_API_KEY")
