import streamlit as st
import requests

st.set_page_config(page_title="FinSolve Chatbot")
st.title("🤖 FinSolve Chatbot")

# Initialize session state for username, role, password, and messages
if "username" not in st.session_state:
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.password = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # stores (question, answer)

# Login page
if st.session_state.username == "":
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.get("http://127.0.0.1:8000/login", auth=(username, password))
        if res.status_code == 200:
            data = res.json()
            st.session_state.username = username
            st.session_state.role = data["role"]
            st.session_state.password = password
            st.success(f"✅ Logged in as: {username} | Role: {data['role']}")
        else:
            st.error("❌ Login failed. Please check username/password.")

else:
    st.subheader(f"Welcome, {st.session_state.username} 👋 (Role: {st.session_state.role})")

    question = st.text_input("Ask me something:")

    if st.button("Ask"):
        res = requests.post(
            "http://127.0.0.1:8000/chat",
            params={"message": question},
            auth=(st.session_state.username, st.session_state.password)
        )
        if res.status_code == 200:
            data = res.json()
            answer = data["answer"]
            sources = ', '.join(data['sources'])
            # Add to chat history
            st.session_state.chat_history.append((question, answer, sources))
        else:
            st.error("⚠️ Error getting answer from backend.")

    # Display chat history
    if st.session_state.chat_history:
        st.write("---")
        for i, (q, a, s) in enumerate(reversed(st.session_state.chat_history), 1):
            st.write(f"**❓ Q{i}:** {q}")
            st.write(f"**🤖 A{i}:** {a}")
            st.caption(f"📄 Sources: {s}")

    # Buttons: clear chat and logout
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Clear chat"):
            st.session_state.chat_history = []
    with col2:
        if st.button("🔒 Logout"):
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.password = ""
            st.session_state.chat_history = []
            
