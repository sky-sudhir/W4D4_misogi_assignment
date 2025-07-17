import chromadb
from chromadb.config import Settings


client = chromadb.CloudClient(
  api_key='apikey',
  tenant='apikey',
  database='hrm'
)
collection = client.get_or_create_collection("hr-docs")

def add_to_vector_store(chunks, metadata_list):
    for chunk, metadata in zip(chunks, metadata_list):
        collection.add(
            documents=[chunk],
            metadatas=[metadata],
            # embeddings=[get_embedding(chunk)],
            ids=[f"{metadata['doc_id']}_{metadata['chunk_id']}"]
        )

def search_similar(query, top_k=5):
    return collection.query(query_texts=[query], n_results=top_k)
