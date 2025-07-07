# chroma_utils.py
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

client = chromadb.CloudClient(
  api_key='API_KEY',
  tenant='TENENT',
  database='DB'
)
# collection = client.get_or_create_collection("lecture")
embedding_fn = DefaultEmbeddingFunction()
collection = client.get_or_create_collection(name="lecture_chunks", embedding_function=embedding_fn)

def store_chunks(video_id: str, chunks):
    for idx, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk['text']],
            metadatas=[{
                "video_id": video_id,
                "start": chunk['start'],
                "end": chunk['end']
            }],
            ids=[f"{video_id}_{idx}"]
        )

def query_chunks(query: str, video_id: str|None = None):
    results = collection.query(
        query_texts=[query],
        n_results=5,
        where={"video_id": video_id} if video_id else None
    )
    return results
