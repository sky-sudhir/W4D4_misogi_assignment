from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from uuid import uuid4
import shutil

from utils import extract_audio,generate_response
from transcription import transcribe_audio
from chunker import chunk_transcript
from chroma_utils import store_chunks, query_chunks
from pydantic import BaseModel

app = FastAPI()

# CORS for Streamlit local access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("./data")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_id = str(uuid4())
    video_path = UPLOAD_DIR / f"{video_id}.mp4"
    audio_path = UPLOAD_DIR / f"{video_id}.wav"
    print("saving video")
    # Save uploaded file
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print("video saved")
    # Extract audio
    print("extracting audio")
    extract_audio(str(video_path), str(audio_path))
    print("audio extracted")
    # Transcribe
    transcript_segments = transcribe_audio(str(audio_path))
    print("transcript done")
    # Chunk transcript
    print("chunking transcript")
    chunks = chunk_transcript(transcript_segments)
    print("chunks done")
    # Store in ChromaDB
    store_chunks(video_id, chunks)
    print("chunks stored")
    return {"status": "success", "video_id": video_id, "chunks_stored": len(chunks)}

class QueryRequest(BaseModel):
    query: str
    video_id: str|None = None

@app.post("/query")
def query_lecture(req: QueryRequest):
    print("querying chunks")
    if req.video_id:
        chunks = query_chunks(req.query, req.video_id)
    else:
        chunks = query_chunks(req.query)
    print("chunks queried")
    answer = generate_response(req.query, chunks)
    print("answer generated")
    return {"answer": answer, "chunks": chunks}