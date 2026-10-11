import streamlit as st
from config import LANGUAGES
from utils.audio_utils import text_to_speech
from utils.translator_utils import translate_text


def render():
    st.markdown('<div class="glass-card"><h2>🔊 Text To Speech</h2>'
                 '<p>Convert any text into natural-sounding audio and download it as MP3.</p></div>',
                unsafe_allow_html=True)

    lang_codes = [c for c in LANGUAGES if c != "auto"]
    text = st.text_area("Enter text", height=150, placeholder="Type text here...")

    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("Speak in this language", lang_codes, format_func=lambda c: LANGUAGES[c])
    with col2:
        slow = st.checkbox("🐢 Slow playback")

    auto_translate = st.checkbox(
        "🌐 Translate my text into the selected language before speaking",
        value=True,
        help="Turn this ON if you typed text in one language (e.g. English) but want it "
             "spoken in another (e.g. Hindi). Turn it OFF only if your typed text is already "
             "in the selected language."
    )

    if st.button("🔊 Generate Audio", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Preparing audio..."):
                try:
                    final_text = text
                    if auto_translate:
                        final_text = translate_text(text, source="auto", target=lang)
                    st.session_state.tts_final_text = final_text
                    audio_path = text_to_speech(final_text, lang=lang, slow=slow)
                    st.session_state.tts_audio_path = audio_path
                except Exception as e:
                    st.error(f"Could not generate audio: {e}")

    if st.session_state.get("tts_audio_path"):
        if auto_translate and st.session_state.get("tts_final_text"):
            st.markdown(f"""<div class="output-card"><b>Spoken text ({LANGUAGES[lang]}):</b>
                        <p>{st.session_state.tts_final_text}</p></div>""", unsafe_allow_html=True)
        st.markdown("#### ▶ Playback")
        st.audio(st.session_state.tts_audio_path)
        with open(st.session_state.tts_audio_path, "rb") as f:
            st.download_button("⬇ Download MP3", f, file_name="translation_audio.mp3", mime="audio/mp3")
