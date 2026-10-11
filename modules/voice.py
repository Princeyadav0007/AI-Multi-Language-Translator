import streamlit as st
import tempfile
import os
from config import LANGUAGES
from utils.speech_utils import recognize_from_microphone, recognize_from_file
from utils.translator_utils import translate_text, detect_language
from utils.database import add_entry
from utils.audio_utils import text_to_speech

SPEECH_LANG_MAP = {  # BCP-47 codes for the speech recognizer
    "en": "en-US", "hi": "hi-IN", "es": "es-ES", "fr": "fr-FR", "de": "de-DE",
    "ur": "ur-PK", "ar": "ar-SA", "zh-CN": "zh-CN", "ja": "ja-JP", "ko": "ko-KR",
    "ru": "ru-RU", "pt": "pt-PT", "it": "it-IT", "bn": "bn-IN", "ta": "ta-IN",
    "te": "te-IN", "mr": "mr-IN", "gu": "gu-IN", "pa": "pa-IN", "kn": "kn-IN",
}


def render():
    st.markdown('<div class="glass-card"><h2>🎤 Voice Translation</h2>'
                 '<p>Speak (or upload an audio clip) and get an instant translation.</p></div>',
                unsafe_allow_html=True)

    lang_codes = [c for c in LANGUAGES if c != "auto"]
    col1, col2 = st.columns(2)
    with col1:
        speak_lang = st.selectbox("You are speaking in", lang_codes,
                                   format_func=lambda c: LANGUAGES[c], index=lang_codes.index("en"))
    with col2:
        target_lang = st.selectbox("Translate to", lang_codes,
                                    format_func=lambda c: LANGUAGES[c], index=lang_codes.index("hi"))

    st.markdown("#### Option A — Record with Microphone (run locally)")
    st.caption("Note: microphone recording only works when the app is run on your own computer "
               "(`streamlit run app.py`), not in a hosted/cloud environment without mic access.")
    rec_col1, rec_col2 = st.columns(2)
    start = rec_col1.button("🎤 Start Recording", use_container_width=True)
    rec_col2.button("⏹ Stop / Reset", use_container_width=True,
                     on_click=lambda: st.session_state.pop("voice_text", None))

    if start:
        with st.spinner("Listening... speak now"):
            try:
                text = recognize_from_microphone(language=SPEECH_LANG_MAP.get(speak_lang, "en-US"))
                st.session_state.voice_text = text
            except Exception as e:
                st.error(str(e))

    st.markdown("#### Option B — Upload an Audio File")
    audio_file = st.file_uploader("Upload WAV / AIFF / FLAC audio", type=["wav", "aiff", "flac"])
    if audio_file and st.button("📤 Transcribe Uploaded Audio"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        with st.spinner("Transcribing..."):
            try:
                text = recognize_from_file(tmp_path, language=SPEECH_LANG_MAP.get(speak_lang, "en-US"))
                st.session_state.voice_text = text
            except Exception as e:
                st.error(str(e))
            finally:
                os.unlink(tmp_path)

    if st.session_state.get("voice_text"):
        st.markdown(f"""<div class="glass-card"><b>🗣 Recognized Speech:</b><p>{st.session_state.voice_text}</p></div>""",
                    unsafe_allow_html=True)

        with st.spinner("Auto-translating..."):
            try:
                result = translate_text(st.session_state.voice_text, source=speak_lang, target=target_lang)
                add_entry(st.session_state.voice_text, result, speak_lang, target_lang)
            except Exception as e:
                st.error(str(e))
                result = None

        if result:
            st.markdown(f"""
            <div class="output-card">
                <span class="badge">{LANGUAGES[speak_lang]} → {LANGUAGES[target_lang]}</span>
                <p style="margin-top:12px; font-size:1.15rem;">{result}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔊 Listen to Translation", key="voice_listen"):
                try:
                    audio_path = text_to_speech(result, lang=target_lang)
                    st.audio(audio_path)
                except Exception as e:
                    st.error(f"Could not generate audio: {e}")
