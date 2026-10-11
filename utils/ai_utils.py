"""
Module 6: AI Expression Detection (rule-based NLP)
Module 7: AI Learning Chatbot (grammar correction via LanguageTool)
"""
import re

# ---------------------------------------------------------------------
# Module 6 — AI Expression Detection
# ---------------------------------------------------------------------

GREETING_WORDS = {
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
    "namaste", "greetings", "yo", "what's up",
}

IDIOM_DICTIONARY = {
    "break a leg": "Good luck",
    "piece of cake": "Something very easy",
    "hit the books": "To study hard",
    "under the weather": "Feeling sick",
    "spill the beans": "Reveal a secret",
    "once in a blue moon": "Something that rarely happens",
    "cost an arm and a leg": "Very expensive",
    "hit the sack": "Go to sleep",
    "let the cat out of the bag": "Reveal a secret accidentally",
    "on cloud nine": "Extremely happy",
    "the ball is in your court": "It's your decision now",
    "bite the bullet": "Face a difficult situation bravely",
}

COMMAND_STARTERS = {
    "go", "stop", "come", "sit", "run", "please", "close", "open", "take",
    "give", "bring", "call", "start", "wait", "listen", "look", "turn",
    "do", "don't", "let", "move", "help",
}


def detect_expression(text: str) -> dict:
    """
    Analyze the input text and classify it as:
    idiom / question / greeting / command / exclamation / statement / phrase / quote
    Returns a dict with type, meaning (if any) and a confidence score.
    """
    if not text or not text.strip():
        return {"type": "Unknown", "meaning": None, "confidence": 0.0}

    stripped = text.strip()
    lower = stripped.lower().strip(" .!?")

    # 1. Idiom check (highest priority — exact/partial match in dictionary)
    for idiom, meaning in IDIOM_DICTIONARY.items():
        if idiom in lower:
            return {"type": "Idiom", "meaning": meaning, "confidence": 0.95}

    # 2. Quote check (wrapped in quotation marks)
    if (stripped.startswith('"') and stripped.endswith('"')) or \
       (stripped.startswith("'") and stripped.endswith("'")):
        return {"type": "Quote", "meaning": "A quoted phrase or citation", "confidence": 0.85}

    # 3. Question check
    if stripped.endswith("?") or lower.split()[0] in {
        "what", "why", "how", "when", "where", "who", "which", "can", "could",
        "would", "should", "is", "are", "do", "does", "did", "will"
    }:
        return {"type": "Question", "meaning": "The speaker is asking something", "confidence": 0.9}

    # 4. Exclamation check
    if stripped.endswith("!"):
        return {"type": "Exclamation", "meaning": "An expression of strong emotion", "confidence": 0.85}

    # 5. Greeting check
    if lower in GREETING_WORDS or any(lower.startswith(g) for g in GREETING_WORDS):
        return {"type": "Greeting", "meaning": "A polite opening expression", "confidence": 0.9}

    # 6. Command check
    first_word = lower.split()[0] if lower.split() else ""
    if first_word in COMMAND_STARTERS:
        return {"type": "Command", "meaning": "An instruction or request for action", "confidence": 0.75}

    # 7. Phrase vs Statement (a phrase has no verb / is short & incomplete)
    word_count = len(lower.split())
    if word_count <= 3 and not re.search(r"\b(is|are|was|were|am|do|does|did|has|have|will)\b", lower):
        return {"type": "Phrase", "meaning": "A short expression, not a full sentence", "confidence": 0.6}

    # 8. Default: statement
    return {"type": "Statement", "meaning": "A regular declarative sentence", "confidence": 0.8}


# ---------------------------------------------------------------------
# Module 7 — AI Learning Chatbot (Real LLM via Groq — free API)
# ---------------------------------------------------------------------

import os
import base64
import requests

try:
    import streamlit as st
except ImportError:
    st = None

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"  # llama-3.3-70b-versatile was deprecated by Groq
GROQ_VISION_MODEL = "qwen/qwen3.8-27b"

TUTOR_SYSTEM_PROMPT = (
    "You are a friendly, encouraging English-learning tutor inside a translator app. "
    "The user will chat with you naturally — any topic, any sentence, real conversation, "
    "not fixed templates. For every message from the user: "
    "1) If there are grammar or spelling mistakes, gently point them out and show the corrected sentence. "
    "2) Briefly explain the mistake in very simple words. "
    "3) Suggest a more natural or professional way to phrase it if relevant. "
    "4) Keep the conversation going naturally like a real chat, don't just robotically correct — "
    "also answer their question or respond to what they said. "
    "Keep replies concise (3-6 sentences), warm, and easy to understand for a language learner."
)


def get_groq_api_key():
    """Read the Groq API key from Streamlit secrets (cloud) or an env var (local)."""
    if st is not None:
        try:
            if "GROQ_API_KEY" in st.secrets:
                return st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    return os.getenv("GROQ_API_KEY")


def ask_ai_tutor(conversation_history: list) -> str:
    """
    Send the full chat history to Groq's free LLM API and get a real,
    context-aware reply — not a fixed/templated response.
    conversation_history: list of {"role": "user"/"assistant", "content": str}
    """
    api_key = get_groq_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Get a free key from https://console.groq.com/keys "
            "and add it to .streamlit/secrets.toml (or your .env file)."
        )

    messages = [{"role": "system", "content": TUTOR_SYSTEM_PROMPT}] + conversation_history

    response = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": GROQ_MODEL, "messages": messages, "temperature": 0.4, "max_tokens": 500},
        timeout=25,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------
# Image Text Extraction (OCR) — reuses the same Groq API via a
# vision-capable model, so no separate OCR library/API is needed.
# ---------------------------------------------------------------------

def extract_text_from_image(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """
    Extract visible text from an uploaded image using Groq's vision-capable
    LLM (same GROQ_API_KEY already used for the AI Learning Chatbot).
    Returns the extracted text, or "" if no readable text was found.
    """
    api_key = get_groq_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Get a free key from https://console.groq.com/keys "
            "and add it to .streamlit/secrets.toml (or your .env file)."
        )

    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64_image}"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Extract all readable text from this image exactly as it appears, "
                        "preserving line breaks. Return ONLY the extracted text with no "
                        "extra commentary or explanation. If there is no readable text, "
                        "respond with exactly: NO_TEXT_FOUND"
                    ),
                },
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }
    ]

    response = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": GROQ_VISION_MODEL, "messages": messages, "temperature": 0.0, "max_tokens": 800},
        timeout=30,
    )
    if not response.ok:
        try:
            error_detail = response.json().get("error", {}).get("message", response.text)
        except Exception:
            error_detail = response.text
        raise RuntimeError(f"Groq API error ({response.status_code}): {error_detail}")
    data = response.json()
    text = data["choices"][0]["message"]["content"].strip()
    return "" if text == "NO_TEXT_FOUND" else text

