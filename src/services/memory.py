"""Hafıza katmanı: analiz arşivi + önbellek (SQLite)."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src import config

_SCHEMA = """
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER NOT NULL,
    media_type TEXT NOT NULL,
    title TEXT NOT NULL,
    year TEXT,
    report_md TEXT NOT NULL,
    analysis_json TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (tmdb_id, media_type)
);
"""


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(_SCHEMA)
    return conn


def get_cached(media_type: str, tmdb_id: int) -> dict | None:
    """Aynı yapım daha önce analiz edildiyse raporu önbellekten döndürür."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM analyses WHERE tmdb_id = ? AND media_type = ?",
            (tmdb_id, media_type),
        ).fetchone()
    return dict(row) if row else None


def save_analysis(details: dict, report_md: str, analysis: dict) -> None:
    with _connect() as conn:
        conn.execute(
            """INSERT INTO analyses (tmdb_id, media_type, title, year, report_md, analysis_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT (tmdb_id, media_type) DO UPDATE SET
                 report_md = excluded.report_md,
                 analysis_json = excluded.analysis_json,
                 created_at = excluded.created_at""",
            (
                details["tmdb_id"],
                details["media_type"],
                details["title"],
                details.get("year", ""),
                report_md,
                json.dumps(analysis, ensure_ascii=False),
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ),
        )


def list_analyses(limit: int = 20) -> list[dict]:
    """Geçmiş Analizler ekranı için özet liste (yeniden eskiye)."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, tmdb_id, media_type, title, year, created_at FROM analyses "
            "ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_analysis(analysis_id: int) -> dict | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    return dict(row) if row else None
