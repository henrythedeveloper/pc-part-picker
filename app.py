import streamlit as st
from components.chat_interface import chat_with_bot

st.set_page_config(page_title="PC Part Picker", page_icon="🖥️", layout="wide")

st.title("🖥️ PC Part Picker")

# Introduction
st.write("""
Welcome to the PC Part Picker! Provide your budget and preferences, and our assistant will suggest a PC build tailored for you.
""")

# Chatbot Interface
chat_with_bot()
