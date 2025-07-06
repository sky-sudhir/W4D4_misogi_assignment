import streamlit as st
import requests
import os
from pathlib import Path

st.set_page_config(page_title="Lecture QA Assistant", layout="centered")
st.title("🎓 Lecture QA Assistant")

# Backend API URL
BACKEND_URL = "http://localhost:8000"

# Temp video cache path
VIDEO_CACHE = Path(".cache")
VIDEO_CACHE.mkdir(exist_ok=True)

# Video upload
st.header("Upload a Lecture Video")
video_file = st.file_uploader("Upload MP4 file", type=["mp4"])

video_bytes = None
video_id = None

if video_file:
    st.success("✅ Video uploaded. Sending to backend...")
    files = {"file": (video_file.name, video_file, "video/mp4")}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)
    if response.status_code == 200:
        result = response.json()
        st.success(f"✅ Processed and stored {result['chunks_stored']} chunks for search!")
        video_id = result['video_id']

        # Save locally for player
        video_path = VIDEO_CACHE / f"{video_id}.mp4"
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        video_bytes = video_path.read_bytes()

        st.video(video_bytes)
    else:
        st.error("❌ Upload failed.")

# Ask a question
st.header("Ask a Question About the Lecture")
question = st.text_input("Enter your question")

if question:
    with st.spinner("Retrieving answer..."):
        res = requests.post(f"{BACKEND_URL}/query", json={"query": question})
        if res.status_code == 200:
            data = res.json()
            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Referenced Lecture Segments")
            for chunk in data["chunks"]:
                start_time = int(chunk['start'])
                minutes = start_time // 60
                seconds = start_time % 60
                timestamp = f"{minutes:02}:{seconds:02}"
                st.markdown(
                    f"- ⏱️ **[{timestamp}](#)** → `{chunk['text'][:200]}...`",
                    unsafe_allow_html=True
                )
        else:
            st.error("❌ Failed to retrieve answer.")
