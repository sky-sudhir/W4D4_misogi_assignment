from vector_store import search_similar
import requests

def generate_response(question: str):
    results = search_similar(question, top_k=3)
    context = "\n\n".join(results["documents"][0])

    prompt = f"""
    You are an HR assistant. Answer the question based on the following HR policies.
    <context>
    {context}
    </context>
    <question>
    {question}
    </question>
    Also provide source citations based on the metadata.
    Answer:
    """

    print(prompt)
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen:4b",
        "prompt": prompt,
        "stream": False
    })

    return res.json()["response"]
