"""
Module 1: Project Setup
Central configuration for the AI Powered Multi-Language Translator.
"""
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "AI Powered Multi-Language Translator")
DEFAULT_SOURCE_LANG = os.getenv("DEFAULT_SOURCE_LANG", "auto")
DEFAULT_TARGET_LANG = os.getenv("DEFAULT_TARGET_LANG", "en")

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "history.db")

# Supported languages (code : name) — used across the app for dropdowns
# Exactly the 20 required languages, plus "auto" (existing detect-language option)
LANGUAGES = {
    "auto": "Detect Language",
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh-CN": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "bn": "Bengali",
    "pa": "Punjabi",
    "gu": "Gujarati",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ur": "Urdu",
}

THEME = {
    "primary": "#7C3AED",
    "primary_light": "#A78BFA",
    "bg_dark": "#0F1117",
    "card_bg": "rgba(255, 255, 255, 0.06)",
    "text": "#F5F5F7",
}
