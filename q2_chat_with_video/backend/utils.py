import requests
import subprocess

def extract_audio(video_path: str, audio_path: str):
    command = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
    ]
    subprocess.run(command, check=True)



def generate_response(question: str, chunks: list):
    context = "\n\n".join(chunks["documents"][0])

    prompt = f"""
    You are an AI assistant. Answer the question based on the following lecture.
    <context>
    {context}
    </context>
    <question>
    {question}
    </question>
    Answer:
    """

    print(prompt)
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen:4b",
        "prompt": prompt,
        "stream": False
    })

    return res.json()["response"]
