"""
Module 3: Translation Engine.
Wraps deep-translator's GoogleTranslator (free, no API key needed), with an
automatic fallback to MyMemory (a second, independent free translation
service) if Google's free endpoint is temporarily rate-limited.
"""
import time
from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # deterministic results

# MyMemory's free API needs locale-specific codes (e.g. "en-GB", "hi-IN"),
# not plain ISO codes — this maps our app's language codes to MyMemory's.
MYMEMORY_LANG_MAP = {
    "en": "en-GB", "hi": "hi-IN", "es": "es-ES", "fr": "fr-FR", "de": "de-DE",
    "it": "it-IT", "pt": "pt-PT", "ru": "ru-RU", "zh-CN": "zh-CN", "ja": "ja-JP",
    "ko": "ko-KR", "ar": "ar-SA", "bn": "bn-IN", "pa": "pa-IN", "gu": "gu-IN",
    "mr": "mr-IN", "ta": "ta-IN", "te": "te-IN", "kn": "kn-IN", "ur": "ur-PK",
}


def detect_language(text: str) -> str:
    """Detect the source language code of the given text (offline, via langdetect)."""
    try:
        return detect(text)
    except Exception:
        return "auto"


def _translate_with_google(text: str, source: str, target: str) -> str:
    last_error = None
    for attempt in range(3):
        try:
            result = GoogleTranslator(source=source, target=target).translate(text)
            return result or ""
        except LanguageNotSupportedException:
            raise ValueError("One of the selected languages is not supported.")
        except Exception as e:
            last_error = e
            if "too many requests" in str(e).lower() and attempt < 2:
                time.sleep(2 * (attempt + 1))  # brief backoff, then retry
                continue
            break
    raise RuntimeError(str(last_error))


def _translate_with_mymemory(text: str, source: str, target: str) -> str:
    # MyMemory needs a real, locale-specific source language code —
    # it doesn't understand "auto" or plain 2-letter codes like "en".
    resolved_source = detect_language(text) if source == "auto" else source
    mm_source = MYMEMORY_LANG_MAP.get(resolved_source, "en-GB")
    mm_target = MYMEMORY_LANG_MAP.get(target, target)
    result = MyMemoryTranslator(source=mm_source, target=mm_target).translate(text)
    return result or ""


def translate_text(text: str, source: str = "auto", target: str = "en") -> str:
    """Translate text from source language to target language.
    Tries Google Translate first (with short retries), and automatically
    falls back to MyMemory (an independent free service) if Google's free
    endpoint is temporarily rate-limited or unreachable."""
    if not text or not text.strip():
        return ""

    try:
        return _translate_with_google(text, source, target)
    except ValueError:
        raise  # unsupported language — no point falling back
    except Exception as google_error:
        try:
            return _translate_with_mymemory(text, source, target)
        except Exception as mymemory_error:
            raise RuntimeError(
                "Both translation services failed.\n"
                f"- Google: {google_error}\n"
                f"- MyMemory: {mymemory_error}\n\n"
                "This usually means either (a) no internet connection right now, "
                "(b) a firewall/antivirus/VPN is blocking the request, or "
                "(c) you're genuinely rate-limited — wait a minute and retry."
            )


def swap_languages(source: str, target: str):
    """Swap source and target language codes (auto cannot be a target)."""
    if source == "auto":
        return target, "en"
    return target, source
