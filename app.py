"""Media Mirror — Streamlit arayüzü."""
import json

import streamlit as st

from src import config
from src.pipeline import Pipeline
from src.services import memory, tmdb
from src.services.card import generate_card

st.set_page_config(page_title="Media Mirror", page_icon="🪞", layout="centered")


def run_analysis(item: dict) -> None:
    """Seçilen yapım için önbellek kontrolü + pipeline çalıştırma."""
    cached = memory.get_cached(item["media_type"], item["tmdb_id"])
    if cached:
        st.session_state.report_view = {
            "title": cached["title"],
            "year": cached["year"],
            "media_type": cached["media_type"],
            "report_md": cached["report_md"],
            "analysis": json.loads(cached["analysis_json"] or "{}"),
            "source": "önbellek",
        }
        return

    pipeline = Pipeline(config.tmdb_api_key(), config.gemini_api_key())
    with st.status("Agent pipeline'ı çalışıyor…", expanded=True) as status:
        try:
            result = pipeline.run(
                item["media_type"], item["tmdb_id"], on_step=st.write
            )
        except Exception as exc:
            status.update(label="Analiz başarısız", state="error")
            st.error(f"Analiz tamamlanamadı: {exc}")
            return
        status.update(label="Analiz tamamlandı", state="complete", expanded=False)

    if not result["honest_refusal"]:
        memory.save_analysis(result["details"], result["report_md"], result["analysis"])

    st.session_state.report_view = {
        "title": result["details"]["title"],
        "year": result["details"]["year"],
        "media_type": result["details"]["media_type"],
        "report_md": result["report_md"],
        "analysis": {} if result["honest_refusal"] else result["analysis"],
        "source": "düzeltme turlu analiz" if result["revised"] else "analiz",
    }


# ── Kenar çubuğu: durum + Geçmiş Analizler ──────────────────────────────
with st.sidebar:
    st.header("🪞 Media Mirror")
    st.caption("Filmlerin ve dizilerin kadın karakterlerine feminist bir bakış.")

    missing = [
        name
        for name, key in (
            ("TMDB_API_KEY", config.tmdb_api_key()),
            ("GEMINI_API_KEY", config.gemini_api_key()),
        )
        if not key
    ]
    if missing:
        st.error("Eksik anahtar: " + ", ".join(missing) + "\n\n`.env` dosyasını doldurun.")

    st.subheader("🗂️ Geçmiş Analizler")
    past = memory.list_analyses()
    if not past:
        st.caption("Henüz analiz yok.")
    for row in past:
        label = f"{row['title']} ({row['year'] or '?'})"
        if st.button(label, key=f"past_{row['id']}", use_container_width=True):
            full = memory.get_analysis(row["id"])
            st.session_state.report_view = {
                "title": full["title"],
                "year": full["year"],
                "media_type": full["media_type"],
                "report_md": full["report_md"],
                "analysis": json.loads(full["analysis_json"] or "{}"),
                "source": "arşiv",
            }

# ── Ana akış: arama → seçim → rapor ─────────────────────────────────────
st.title("🪞 Media Mirror")
st.write(
    "Bir film ya da dizi adı yazın; kadın karakterlerin anlatıdaki konumunu, "
    "ajansını ve üzerlerine yüklenen klişeleri feminist perspektiften analiz edelim."
)

with st.form("search_form"):
    query = st.text_input("Film / dizi adı", placeholder="örn. Fleabag, Kış Uykusu…")
    submitted = st.form_submit_button("Ara", type="primary", disabled=bool(missing))

if submitted and query.strip():
    st.session_state.pop("report_view", None)
    try:
        st.session_state.search_results = tmdb.search(query.strip(), config.tmdb_api_key())
    except tmdb.TMDbError as exc:
        st.error(str(exc))
        st.session_state.search_results = []
    if not st.session_state.search_results:
        st.warning("Sonuç bulunamadı. Başlığı farklı yazarak tekrar deneyin.")

results = st.session_state.get("search_results") or []
if results and "report_view" not in st.session_state:
    st.subheader("Hangi yapımı kastettiniz?")
    for item in results:
        col_poster, col_info = st.columns([1, 4])
        with col_poster:
            if item["poster_url"]:
                st.image(item["poster_url"], width=90)
            else:
                st.markdown("🎞️")
        with col_info:
            kind = "Film" if item["media_type"] == "movie" else "Dizi"
            st.markdown(f"**{item['title']}** ({item['year']}) · {kind}")
            if item["overview"]:
                st.caption(item["overview"][:200] + ("…" if len(item["overview"]) > 200 else ""))
            if st.button("Bu yapımı analiz et", key=f"sel_{item['media_type']}_{item['tmdb_id']}"):
                run_analysis(item)
                st.rerun()
        st.divider()

view = st.session_state.get("report_view")
if view:
    st.header(f"{view['title']} ({view['year']})")
    if view["source"] in ("önbellek", "arşiv"):
        st.info(f"Bu rapor {view['source']}ten anında yüklendi. 🗂️")
    st.markdown(view["report_md"])

    if view.get("analysis"):
        st.divider()
        try:
            card_png = generate_card(
                view["title"], view["year"], view.get("media_type", "movie"), view["analysis"]
            )
        except Exception:
            card_png = None
        if card_png:
            with st.expander("📸 Paylaşılabilir özet kart"):
                st.image(card_png, width=420)
                st.download_button(
                    "Kartı indir (PNG)",
                    data=card_png,
                    file_name=f"media-mirror-{view['title'].lower().replace(' ', '-')}.png",
                    mime="image/png",
                )
