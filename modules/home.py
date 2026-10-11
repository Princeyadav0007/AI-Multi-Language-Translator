import streamlit as st
from utils.database import get_all


def render():
    st.markdown("""
    <div class="glass-card">
        <h2>Welcome 👋</h2>
        <p>This is an AI Powered Multi-Language Translator built for the mini project. It combines text translation, voice translation,
        text-to-speech, NLP-based expression detection, and an AI English-learning
        chatbot — all in one app.</p>
    </div>
    """, unsafe_allow_html=True)

    rows = get_all()
    total = len(rows)
    favorites = len([r for r in rows if r[4] == 1])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="glass-card"><h3>📚</h3><h2>{total}</h2><p>Total Translations</p></div>""",
                     unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="glass-card"><h3>⭐</h3><h2>{favorites}</h2><p>Favorites</p></div>""",
                     unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="glass-card"><h3>🌍</h3><h2>20+</h2><p>Languages Supported</p></div>""",
                     unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="glass-card"><h3>🤖</h3><h2>10</h2><p>Modules Integrated</p></div>""",
                     unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h3>🧭 Explore the App</h3>
        <span class="badge">🌍 Translator</span>
        <span class="badge">🎤 Voice Translation</span>
        <span class="badge">🤖 AI Learning</span>
        <span class="badge">📚 History</span>
        <span class="badge">⚙ Settings</span>
        <p style="margin-top:14px;">Use the sidebar to navigate between features.</p>
    </div>
    """, unsafe_allow_html=True)
