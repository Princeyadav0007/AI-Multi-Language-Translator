import streamlit as st
from utils.ai_utils import detect_expression
from utils.translator_utils import detect_language
from config import LANGUAGES


def render():
    st.markdown('<div class="glass-card"><h2>🧠 AI Expression Detection</h2>'
                 '<p>Analyze a sentence to detect whether it\'s a question, idiom, greeting, '
                 'command, statement, and more.</p></div>', unsafe_allow_html=True)

    text = st.text_input("Enter a sentence or phrase", placeholder="e.g. Break a leg!")

    if st.button("🔍 Analyze", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            result = detect_expression(text)
            try:
                lang = detect_language(text)
                lang_name = LANGUAGES.get(lang, lang)
            except Exception:
                lang_name = "Unknown"

            confidence_pct = int(result["confidence"] * 100)
            st.markdown(f"""
            <div class="output-card">
                <h3>AI Expression Detection</h3>
                <p><b>Language:</b> {lang_name}</p>
                <p><b>Expression Type:</b> <span class="badge">{result['type']}</span></p>
                <p><b>Meaning:</b> {result['meaning'] or '—'}</p>
                <p><b>Confidence:</b> {confidence_pct}%</p>
                <div class="confidence-bar-bg">
                    <div class="confidence-bar-fill" style="width:{confidence_pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("💡 Try these examples"):
        st.code("Break a leg\nCan you help me?\nHello\nPlease close the door\nWow, that's amazing!")
