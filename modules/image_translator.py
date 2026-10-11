import streamlit as st
from config import LANGUAGES
from utils.ai_utils import extract_text_from_image, get_groq_api_key
from utils.translator_utils import translate_text
from utils.database import add_entry


def render():
    st.markdown('<div class="glass-card"><h2>🖼 Image Translator</h2>'
                 '<p>Upload an image containing text — the app will read the text and '
                 'translate it into your selected language.</p></div>', unsafe_allow_html=True)

    if not get_groq_api_key():
        st.warning(
            "⚠️ Image Translator is not configured yet. Get a **free** API key from "
            "[console.groq.com/keys](https://console.groq.com/keys) and add it as `GROQ_API_KEY` "
            "in `.streamlit/secrets.toml` (local) or your app's Secrets (Streamlit Cloud). "
            "This is the same key used by the AI Learning Chatbot."
        )
        return

    lang_codes = [c for c in LANGUAGES if c != "auto"]
    target_lang = st.selectbox(
        "Translate extracted text to", lang_codes,
        format_func=lambda c: LANGUAGES[c],
        index=lang_codes.index("en"),
    )

    image_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if image_file:
        st.image(image_file, caption="Uploaded Image")

        if st.button("🔍 Extract & Translate", use_container_width=True):
            with st.spinner("Reading text from image..."):
                try:
                    image_bytes = image_file.getvalue()
                    mime_type = image_file.type or "image/png"
                    extracted_text = extract_text_from_image(image_bytes, mime_type)
                except Exception as e:
                    st.error(f"Could not read text from image: {e}")
                    extracted_text = None

            if extracted_text is not None:
                if not extracted_text.strip():
                    st.warning("No readable text was found in this image.")
                else:
                    st.markdown("#### 📝 Extracted Text")
                    st.markdown(f'<div class="glass-card">{extracted_text}</div>', unsafe_allow_html=True)

                    with st.spinner("Translating..."):
                        try:
                            translated = translate_text(extracted_text, source="auto", target=target_lang)
                            add_entry(extracted_text, translated, "auto", target_lang)
                        except Exception as e:
                            st.error(str(e))
                            translated = None

                    if translated:
                        st.markdown("#### 🌍 Translated Text")
                        st.markdown(f"""
                        <div class="output-card">
                            <span class="badge">→ {LANGUAGES[target_lang]}</span>
                            <p style="margin-top:12px; font-size:1.15rem;">{translated}</p>
                        </div>
                        """, unsafe_allow_html=True)
