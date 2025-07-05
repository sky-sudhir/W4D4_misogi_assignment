from fastapi import FastAPI, UploadFile, Form
from injestion import extract_text
from vector_store import add_to_vector_store
from qa_pipeline import generate_response
import uuid

app = FastAPI()

@app.post("/upload")
async def upload_doc(file: UploadFile):
    path = f"uploaded_docs/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)
    doc_id = str(uuid.uuid4())

    # Simple fixed-size chunking
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    metadata = [{"doc_id": doc_id, "chunk_id": i, "filename": file.filename} for i in range(len(chunks))]
    add_to_vector_store(chunks, metadata)
    return {"status": "Document uploaded and indexed."}

@app.post("/query")
async def query(question: str = Form(...)):
    answer = generate_response(question)
    return {"answer": answer}
