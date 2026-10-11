# 🌐 AI Powered Multi-Language Translator

A final-year B.Tech (CSE) mini project — a Streamlit web app that combines
text translation, voice translation, text-to-speech, NLP-based expression
detection, and an AI English-learning chatbot, with a modern dark
glassmorphism UI.

## ✨ Features (Modules)

| # | Module | What it does |
|---|--------|---------------|
| 1 | Project Setup | Clean folder structure, config, env vars |
| 2 | Advanced UI | Dark glassmorphism Streamlit UI, sidebar nav |
| 3 | Translation Engine | Detect language + translate between 20+ languages |
| 4 | Voice Translation | Speak or upload audio → auto-translate |
| 5 | Text To Speech | Convert any text to MP3 audio, downloadable |
| 6 | AI Expression Detection | Classifies input as idiom / question / greeting / command / statement etc. |
| 7 | AI Learning Chatbot | Grammar correction, natural/professional rewrites, alternative phrasing |
| 8 | Translation History | SQLite-backed history: search, favorite, delete, export CSV |
| 9 | Settings | Theme, speech speed, default language, cache clearing, service status |
| 10 | Testing & Deployment | Ready for GitHub upload / Streamlit Cloud deployment |

All translation, speech, and grammar services used are **free** — no paid
API keys required.

## 🛠 Tech Stack

- **Frontend/App:** Streamlit
- **Translation:** `deep-translator` (Google Translate, free)
- **Language Detection:** `langdetect`
- **Speech-to-Text:** `SpeechRecognition` (Google Web Speech API)
- **Text-to-Speech:** `gTTS`
- Grammar Checking / AI Chatbot: **LanguageTool free API — replaced with Groq (Llama 3.3) free LLM API** for real, natural conversation
- **Database:** SQLite (built into Python)

## 📁 Folder Structure

```
AI-Multi-Language-Translator/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── css/
│   └── style.css
├── modules/
│   ├── home.py
│   ├── translator.py
│   ├── voice.py
│   ├── tts.py
│   ├── expression_detection.py
│   ├── learning_chatbot.py
│   ├── history.py
│   └── settings.py
├── utils/
│   ├── translator_utils.py
│   ├── speech_utils.py
│   ├── audio_utils.py
│   ├── ai_utils.py
│   └── database.py
└── database/
    └── history.db   (auto-created on first run)
```

## 🚀 Setup & Run (Local Machine)

1. **Install Python 3.9+** if you don't already have it.

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > 🎤 For microphone support you also need `PyAudio`:
   > - Windows: `pip install pyaudio`
   > - macOS: `brew install portaudio && pip install pyaudio`
   > - Linux: `sudo apt-get install portaudio19-dev && pip install pyaudio`

4. **(Optional) Configure environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

6. Open the URL Streamlit prints (usually `http://localhost:8501`).

## ☁️ Deploying (for your project demo/report)

You can deploy free on **Streamlit Community Cloud**:
1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo.
3. Set the main file to `app.py` and deploy.

> Note: microphone recording (live mic) only works on your local machine, not
> on a hosted server (browsers/servers don't expose your mic to Streamlit
> Cloud). The **audio file upload** option in Voice Translation works fine
> when deployed.

## 📸 Screenshots

Add screenshots of each screen here before submission (Home, Translator,
Voice Translation, Expression Detection, AI Learning, History, Settings).

## 📝 Project Report Notes

- This project demonstrates: NLP, speech processing, REST/API integration,
  database design (SQLite), and full-stack Python web app development.
- Suggested viva talking points: how `deep-translator` calls Google's
  translation endpoint, how `SpeechRecognition` streams audio to the Web
  Speech API, how the rule-based expression classifier works, and how
  LanguageTool checks grammar.

## 👤 Author

Final Year B.Tech CSE — Mini Project
