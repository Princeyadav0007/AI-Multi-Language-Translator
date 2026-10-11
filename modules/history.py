import streamlit as st
import pandas as pd
from config import LANGUAGES
from utils.database import get_all, toggle_favorite, delete_entry, clear_all


def render():
    st.markdown('<div class="glass-card"><h2>📚 Translation History</h2>'
                 '<p>View, search, favorite, or delete your past translations.</p></div>',
                unsafe_allow_html=True)

    search = st.text_input("🔎 Search history", placeholder="Search by text...")
    rows = get_all(search=search if search else None)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑 Clear All", use_container_width=True):
            clear_all()
            st.rerun()

    if not rows:
        st.info("No translation history yet. Go translate something!")
        return

    for row in rows:
        entry_id, src_text, tgt_text, src_lang, tgt_lang, favorite, created_at = row
        src_lang_name = LANGUAGES.get(src_lang, src_lang)
        tgt_lang_name = LANGUAGES.get(tgt_lang, tgt_lang)

        with st.container():
            st.markdown(f"""
            <div class="glass-card">
                <span class="badge">{src_lang_name} → {tgt_lang_name}</span>
                <span class="badge">{created_at}</span>
                <p style="margin-top:10px;"><b>Original:</b> {src_text}</p>
                <p><b>Translated:</b> {tgt_text}</p>
            </div>
            """, unsafe_allow_html=True)
            b1, b2, b3 = st.columns([1, 1, 1])
            fav_label = "💛 Unfavorite" if favorite else "🤍 Favorite"
            if b1.button(fav_label, key=f"fav_{entry_id}"):
                toggle_favorite(entry_id, not bool(favorite))
                st.rerun()
            if b2.button("🗑 Delete", key=f"del_{entry_id}"):
                delete_entry(entry_id)
                st.rerun()

    # Download history as CSV
    df = pd.DataFrame(rows, columns=["id", "source_text", "translated_text",
                                      "source_lang", "target_lang", "favorite", "created_at"])
    csv = df.to_csv(index=False).encode("utf-8")
    b3_col = st.columns(1)[0]
    b3_col.download_button("⬇ Download History (CSV)", csv, file_name="translation_history.csv", mime="text/csv")
