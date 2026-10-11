import streamlit as st
from config import APP_NAME
from utils.database import init_db
from modules import home, translator, voice, tts, expression_detection, learning_chatbot, history, settings, image_translator

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database (creates table if not exists)
init_db()

# Load custom CSS
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="app-header">
    <span class="app-logo">🌐</span>
    <h1>{APP_NAME}</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
PAGES = {
    "🏠 Home": home,
    "🌍 Translator": translator,
    "🖼 Image Translator": image_translator,
    "🎤 Voice Translation": voice,
    "🔊 Text To Speech": tts,
    "🧠 Expression Detection": expression_detection,
    "🤖 AI Learning": learning_chatbot,
    "📚 History": history,
    "⚙ Settings": settings,
}

with st.sidebar:
    st.markdown("### 🌐 Navigation")
    choice = st.radio("Go to", list(PAGES.keys()), label_visibility="collapsed")
    st.markdown("---")
    st.caption("AI Powered Multi-Language Translator")
    st.caption("The main objective is not only to translate languages but also to make the system an intelligent language assistant. It combines translation, speech processing and AI-based learning features in a single platform.")

# Render selected page
PAGES[choice].render()
