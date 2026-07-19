"""Paylaşılabilir özet kart üretici (PNG).

LLM kullanmaz; raporun analiz verisinden deterministik olarak 1080x1080
sosyal medya kartı çizer.
"""
from __future__ import annotations

import io

from PIL import Image, ImageDraw, ImageFont

SIZE = 1080
MARGIN = 84

BG = "#241433"
ACCENT = "#E85D8A"
TITLE_COLOR = "#F7F2FA"
TEXT_COLOR = "#D9CFE4"
MUTED = "#9A8BAD"

# Sırasıyla denenir: macOS (geliştirme) ve Debian/Streamlit Cloud (packages.txt ile dejavu)
_FONT_PATHS = {
    "bold": [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "regular": [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}


def _font(kind: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in _FONT_PATHS[kind]:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def generate_card(title: str, year: str, media_type: str, analysis: dict) -> bytes:
    img = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)
    width = SIZE - 2 * MARGIN
    y = MARGIN

    # Üst bant: marka
    brand_font = _font("bold", 30)
    draw.text((MARGIN, y), "MEDIA MIRROR", font=brand_font, fill=ACCENT)
    y += 64

    # Başlık (uzunsa küçült)
    title_size = 76
    while title_size > 40:
        title_font = _font("bold", title_size)
        title_lines = _wrap(draw, title, title_font, width)
        if len(title_lines) <= 3:
            break
        title_size -= 8
    for line in title_lines:
        draw.text((MARGIN, y), line, font=title_font, fill=TITLE_COLOR)
        y += int(title_size * 1.18)

    kind = "Film" if media_type == "movie" else "Dizi"
    meta_font = _font("regular", 34)
    draw.text((MARGIN, y + 6), f"{year} · {kind} · Feminist Mercek Altında", font=meta_font, fill=MUTED)
    y += 76

    # Ayraç
    draw.rectangle([MARGIN, y, MARGIN + 140, y + 6], fill=ACCENT)
    y += 48

    # Durum satırı
    badge_font = _font("bold", 32)
    if analysis.get("kadin_temsili_yok"):
        badge = "KADIN TEMSİLİ: YOK DENECEK DÜZEYDE — BU DA BİR BULGU"
    else:
        n = len(analysis.get("kadin_karakterler") or [])
        badge = f"{n} KADIN KARAKTER ANALİZ EDİLDİ"
    for line in _wrap(draw, badge, badge_font, width):
        draw.text((MARGIN, y), line, font=badge_font, fill=ACCENT)
        y += 44
    y += 24

    # Öne çıkan bulgular (ilk 3)
    body_font = _font("regular", 34)
    for finding in (analysis.get("bulgular") or [])[:3]:
        text = finding if len(finding) <= 220 else finding[:217] + "…"
        lines = _wrap(draw, text, body_font, width - 48)
        draw.text((MARGIN, y), "—", font=_font("bold", 34), fill=ACCENT)
        for line in lines:
            draw.text((MARGIN + 48, y), line, font=body_font, fill=TEXT_COLOR)
            y += 46
        y += 22
        if y > SIZE - 190:
            break

    # Alt bilgi
    footer_font = _font("regular", 27)
    draw.text(
        (MARGIN, SIZE - MARGIN - 30),
        "yapay zeka destekli feminist film ve dizi analizi",
        font=footer_font,
        fill=MUTED,
    )

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
