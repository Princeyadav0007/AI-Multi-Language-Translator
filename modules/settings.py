import streamlit as st
from config import LANGUAGES
from utils.database import clear_all


def render():
    st.markdown('<div class="glass-card"><h2>⚙ Settings</h2>'
                 '<p>Customize your app experience.</p></div>', unsafe_allow_html=True)

    if "settings" not in st.session_state:
        st.session_state.settings = {
            "theme": "Dark",
            "speech_speed": "Normal",
            "default_lang": "en",
        }

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🎨 Theme")
        st.session_state.settings["theme"] = st.radio(
            "Choose theme", ["Dark", "Light"],
            index=0 if st.session_state.settings["theme"] == "Dark" else 1,
            horizontal=True
        )
        if st.session_state.settings["theme"] == "Light":
            st.info("Light mode preference saved. (This build ships with an optimized Dark theme; "
                     "a full Light theme stylesheet can be added in css/style.css.)")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🔊 Speech Speed")
        st.session_state.settings["speech_speed"] = st.select_slider(
            "Text-to-speech playback speed", options=["Slow", "Normal"],
            value=st.session_state.settings["speech_speed"] if st.session_state.settings["speech_speed"] in ["Slow", "Normal"] else "Normal"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🌍 Default Language")
        lang_codes = [c for c in LANGUAGES if c != "auto"]
        st.session_state.settings["default_lang"] = st.selectbox(
            "Default target language", lang_codes,
            index=lang_codes.index(st.session_state.settings["default_lang"]),
            format_func=lambda c: LANGUAGES[c]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🧹 Cache & Data")
        if st.button("Clear Cache & History"):
            clear_all()
            st.cache_data.clear()
            st.success("Cache and history cleared!")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📡 API / Service Status")
        st.markdown("""
        - ✅ Translation Engine (deep-translator / Google): **Free, no key needed**
        - ✅ Speech Recognition (Google Web Speech API): **Free, no key needed**
        - ✅ Text-to-Speech (gTTS): **Free, no key needed**
        - ✅ Grammar Checker (LanguageTool Public API): **Free, no key needed**
        - ℹ All services require an active internet connection.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
