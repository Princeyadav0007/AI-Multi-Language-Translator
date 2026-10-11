"""
Module 5: Text To Speech.
Uses gTTS (Google Text-to-Speech, free, no API key) to generate MP3 audio.
"""
import os
import tempfile
from gtts import gTTS

# gTTS uses its own language codes; most overlap with our LANGUAGES dict.
# A few need remapping (e.g. Chinese simplified).
GTTS_LANG_MAP = {
    "zh-CN": "zh-CN",
    "auto": "en",
}


def text_to_speech(text: str, lang: str = "en", slow: bool = False) -> str:
    """Generate an MP3 file from text and return its file path."""
    if not text or not text.strip():
        raise ValueError("No text provided for speech generation.")

    gtts_lang = GTTS_LANG_MAP.get(lang, lang)
    tts = gTTS(text=text, lang=gtts_lang, slow=slow)

    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, f"tts_output_{abs(hash(text)) % (10**8)}.mp3")
    tts.save(file_path)
    return file_path
