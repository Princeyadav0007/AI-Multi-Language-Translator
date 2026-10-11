import streamlit as st
from config import LANGUAGES
from utils.translator_utils import translate_text, detect_language
from utils.database import add_entry
from utils.audio_utils import text_to_speech


def render():
    st.markdown('<div class="glass-card"><h2>🌍 Translator</h2><p>Translate text between 20+ languages instantly.</p></div>',
                unsafe_allow_html=True)

    if "src_lang" not in st.session_state:
        st.session_state.src_lang = "auto"
    if "tgt_lang" not in st.session_state:
        st.session_state.tgt_lang = "en"
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    lang_codes = list(LANGUAGES.keys())

    col1, col_mid, col2 = st.columns([5, 1, 5])
    with col1:
        st.session_state.src_lang = st.selectbox(
            "Source Language", lang_codes,
            index=lang_codes.index(st.session_state.src_lang),
            format_func=lambda c: LANGUAGES[c], key="src_select"
        )
    with col_mid:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄", help="Swap languages"):
            if st.session_state.src_lang != "auto":
                st.session_state.src_lang, st.session_state.tgt_lang = (
                    st.session_state.tgt_lang, st.session_state.src_lang
                )
                st.rerun()
            else:
                st.warning("Can't swap while source is set to Auto-Detect.")
    with col2:
        tgt_codes = [c for c in lang_codes if c != "auto"]
        st.session_state.tgt_lang = st.selectbox(
            "Target Language", tgt_codes,
            index=tgt_codes.index(st.session_state.tgt_lang) if st.session_state.tgt_lang in tgt_codes else 0,
            format_func=lambda c: LANGUAGES[c], key="tgt_select"
        )

    text = st.text_area("Enter text to translate", height=150, key="input_text",
                         placeholder="Type or paste text here...")

    b1, b2, b3 = st.columns(3)
    translate_clicked = b1.button("✅ Translate", use_container_width=True)
    b2.button("🧹 Clear", use_container_width=True, on_click=lambda: st.session_state.update(input_text=""))
    copy_clicked = b3.button("📋 Copy Translation", use_container_width=True)

    if translate_clicked:
        if not text.strip():
            st.warning("Please enter some text to translate.")
        else:
            with st.spinner("Translating..."):
                try:
                    detected = detect_language(text) if st.session_state.src_lang == "auto" else st.session_state.src_lang
                    result = translate_text(text, source=st.session_state.src_lang, target=st.session_state.tgt_lang)
                    st.session_state.last_translation = result
                    st.session_state.last_detected = detected
                    add_entry(text, result, detected, st.session_state.tgt_lang)
                except Exception as e:
                    st.error(str(e))

    if st.session_state.get("last_translation"):
        detected_name = LANGUAGES.get(st.session_state.get("last_detected", ""), st.session_state.get("last_detected", ""))
        st.markdown(f"""
        <div class="output-card">
            <span class="badge">Detected: {detected_name}</span>
            <span class="badge">→ {LANGUAGES[st.session_state.tgt_lang]}</span>
            <p style="margin-top:12px; font-size:1.15rem;">{st.session_state.last_translation}</p>
        </div>
        """, unsafe_allow_html=True)

        if copy_clicked:
            st.toast("Copied! (select the text above and use Ctrl+C)")

        if st.button("🔊 Listen to Translation"):
            with st.spinner("Generating audio..."):
                try:
                    audio_path = text_to_speech(st.session_state.last_translation, lang=st.session_state.tgt_lang)
                    st.audio(audio_path)
                except Exception as e:
                    st.error(f"Could not generate audio: {e}")
