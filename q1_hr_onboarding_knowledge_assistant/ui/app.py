import streamlit as st
import requests

st.title("🤖 HR Onboarding Knowledge Assistant")

with st.sidebar:
    st.subheader("📄 Upload HR Document")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        res = requests.post("http://localhost:8000/upload", files={"file": uploaded_file})
        st.success(res.json()["status"])

question = st.text_input("💬 Ask your HR question:")

if st.button("Ask"):
    res = requests.post("http://localhost:8000/query", data={"question": question})
    st.markdown("#### 📘 Answer")
    st.write(res.json()["answer"])
