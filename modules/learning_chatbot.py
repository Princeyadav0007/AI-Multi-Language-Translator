import streamlit as st
from utils.ai_utils import ask_ai_tutor, get_groq_api_key


def render():
    st.markdown('<div class="glass-card"><h2>🤖 AI Learning Chatbot</h2>'
                 '<p>Chat naturally in English — ask anything, make mistakes, and get real-time '
                 'corrections and guidance from a real AI tutor (powered by a live LLM).</p></div>',
                unsafe_allow_html=True)

    if not get_groq_api_key():
        st.warning(
            "⚠️ AI Chatbot is not configured yet. Get a **free** API key from "
            "[console.groq.com/keys](https://console.groq.com/keys) and add it as `GROQ_API_KEY` "
            "in `.streamlit/secrets.toml` (local) or your app's Secrets (Streamlit Cloud)."
        )
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type any sentence or message in English...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = ask_ai_tutor(st.session_state.chat_history)
                except Exception as e:
                    reply = f"⚠️ Could not reach the AI service: {e}"
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if st.session_state.chat_history:
        if st.button("🧹 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    with st.expander("💡 Try saying something like this"):
        st.code("I am go to school.\nWhat is meaning of idiom break a leg?\nHow can I improve my spoken English?")
