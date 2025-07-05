# HR Onboarding Knowledge Assistant

Replace time-consuming HR induction calls with an AI-powered assistant that allows new employees to query company policies, benefits, and employment terms from uploaded HR documents.

---

## 🚀 Features

* 📄 Multi-format HR document ingestion (PDF, DOCX, TXT)
* 🧠 Smart text chunking for better context
* 🔍 Vector embedding and similarity search with ChromaDB
* 🤖 AI response generation using Qwen-1.8B via Ollama
* 📚 Citation-based answers from source documents
* 📂 Streamlit UI for document upload and query

---

## 🏗️ Architecture

```
Streamlit UI <--> FastAPI Backend <--> Ollama + ChromaDB
                             \
                              --> Document Parsing + Embedding
```

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **Embeddings:** `nomic-embed-text` via Ollama
* **Vector Store:** ChromaDB
* **LLM:** Qwen-1.8B (via Ollama)
* **Parsing:** PyMuPDF (PDF), python-docx (DOCX)

---

## 📁 Project Structure

```
hr-onboarding-assistant/
├── backend/
│   ├── main.py               # FastAPI app
│   ├── ingestion.py          # Document parsing & chunking
│   ├── embedding.py          # Embedding via Ollama
│   ├── vector_store.py       # ChromaDB operations
│   └── qa_pipeline.py        # RAG pipeline
├── ui/
│   └── app.py                # Streamlit interface
├── data/
│   └── uploaded_docs/        # Uploaded HR documents
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone & Create Environment

```bash
git clone <repo_url>
cd hr-onboarding-assistant
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Backend API

```bash
uvicorn backend.main:app --reload
```

### 4. Start Streamlit Frontend

```bash
streamlit run ui/app.py
```

### 5. Start Ollama (if not running)

```bash
ollama run qwen:1.8b
```

---

## 🔄 Sample Query Use Cases

* "How many vacation days do I get as a new employee?"
* "What's the process for requesting parental leave?"
* "Can I work remotely and what are the guidelines?"
* "How do I enroll in health insurance?"

---

## 📌 Future Improvements

* Admin dashboard to manage documents
* HR-specific smart chunking (based on headings like 'Leave', 'Benefits')
* Query categorization
* Fine-tuning for enterprise HR policies

---

## 👨‍💻 Built With

Made with ❤️ using FastAPI, Chroma, and Qwen.

---

## 📄 License

MIT License
