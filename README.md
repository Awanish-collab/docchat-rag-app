```markdown
# 🧠 DocChat RAG App (Gemini + Pinecone + Supabase + FastAPI + Streamlit)

> 🚀 An end-to-end **Retrieval-Augmented Generation (RAG)** application for interacting with PDFs using **Google Gemini**, **Pinecone**, and **Supabase**, built with **FastAPI** backend and **Streamlit** dashboard frontend.

---

## 📘 Overview

**DocChat RAG App** enables you to upload PDFs, query them in natural language, and visualize analytics — all in real time.

The pipeline performs:
1. PDF extraction → 2. Text chunking → 3. Embedding → 4. Storage in Pinecone  
5. Query retrieval → 6. Gemini LLM generation → 7. Response + analytics logging

This system is fully **containerized (Docker)**, **deployable (Render / Hugging Face)**, and **free-tier compatible**.

---

## 🏗️ System Architecture

```

📄 PDF Upload
↓
🧩 LangChain Text Splitter (Chunking)
↓
🧠 Gemini Embedding Model → Pinecone (Vector DB)
↓
❓ Query → Retrieve Top-k Docs → Gemini Flash (LLM)
↓
✅ Answer + Context + Supabase (for logs)
↓
📊 Streamlit Dashboard (Analytics & Visualization)

```

---

## ⚙️ Technology Stack

| Layer | Tool | Purpose |
|-------|------|----------|
| **LLM + Embeddings** | Google Gemini (AI Studio) | Text generation & vector embeddings |
| **Vector Database** | Pinecone | Store & retrieve embeddings efficiently |
| **Relational Database** | Supabase | Real-time logs & analytics storage |
| **Backend API** | FastAPI + Uvicorn | Serve PDF upload, query & analytics endpoints |
| **Frontend UI** | Streamlit | Chat interface + Upload + Analytics dashboard |
| **Visualization** | Plotly / Altair | Display interactive charts |
| **Deployment** | Docker + Render + GitHub Actions | Containerized, CI/CD automated deployment |
| **Environment Management** | dotenv | Secure API key management |
| **Optional Observability** | LangFuse | Track LLM performance (optional future enhancement) |

---

## 📂 Folder Structure (Development + Deployment Ready)

```

docchat-rag-app/
│
├── 📁 backend/
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # .env loader
│   ├── requirements.txt           # Dependencies
│   │
│   ├── 📁 routes/
│   │   ├── upload_route.py        # /upload endpoint
│   │   ├── query_route.py         # /query endpoint
│   │   └── dashboard_route.py     # /dashboard endpoint
│   │
│   ├── 📁 utils/
│   │   ├── pdf_loader.py          # PDF extraction
│   │   ├── text_splitter.py       # Chunking (LangChain Text Splitter)
│   │   ├── embedding.py           # Gemini Embedding + Pinecone storage
│   │   ├── retriever.py           # Retrieve Top-k docs from Pinecone
│   │   ├── llm_response.py        # Gemini Flash for final answer
│   │   └── logger.py              # Logging helper
│   │
│   ├── 📁 db/
│   │   ├── supabase_client.py     # Real-time query logs
│   │   └── schema.sql             # DB initialization script
│   │
│   ├── 📁 tests/
│   │   └── test_api.py            # API test scripts
│   │
│   ├── Dockerfile
│   └── README.md
│
│
├── 📁 frontend/
│   ├── app.py                     # Main Streamlit app (navigation)
│   │
│   ├── 📁 components/
│   │   ├── upload_component.py    # Upload PDF UI
│   │   ├── chat_component.py      # Chat UI
│   │   └── analytics_component.py # Analytics dashboard
│   │
│   ├── 📁 assets/
│   │   ├── logo.png
│   │   └── styles.css
│   │
│   ├── Dockerfile
│   └── README.md
│
│
├── 📁 data/
│   ├── uploads/                   # User PDFs
│   ├── chunks/                    # Temporary text chunks
│   └── logs/                      # Logs / debugging
│
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── deploy.yml             # GitHub Actions (CI/CD)
│
├── docker-compose.yml             # Orchestrate backend & frontend
├── .env                           # Environment variables
├── .gitignore
├── LICENSE
└── README.md

````

---

## 🖥️ Frontend Screens

| Screen | File | Purpose |
|---------|------|----------|
| **Upload Screen** | `upload_component.py` | Upload PDFs, trigger embedding pipeline |
| **Chat Screen** | `chat_component.py` | Ask questions → retrieve answers from Gemini |
| **Analytics Screen** | `analytics_component.py` | Display Supabase-based metrics (Plotly/Altair) |

```python
# app.py (Main Navigation)
import streamlit as st
from components import upload_component, chat_component, analytics_component

st.sidebar.title("🧠 DocChat RAG App")
page = st.sidebar.radio("Navigate", ["Upload Document", "Chat with Doc", "Analytics Dashboard"])

if page == "Upload Document":
    upload_component.render()
elif page == "Chat with Doc":
    chat_component.render()
else:
    analytics_component.render()
````

---

## 🧩 Backend Endpoints

| Endpoint     | Method | Description                                                |
| ------------ | ------ | ---------------------------------------------------------- |
| `/upload`    | POST   | Accepts a PDF, extracts text, chunks, generates embeddings |
| `/query`     | POST   | Takes user question → retrieves context → generates answer |
| `/dashboard` | GET    | Fetches analytics from Supabase (query logs, usage stats)  |

---

## 🧠 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/docchat-rag-app.git
cd docchat-rag-app
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4️⃣ Configure Environment (.env)

```bash
GEMINI_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

## ⚡ Run Locally

### Run Backend

```bash
cd backend
uvicorn main:app --reload
```

### Run Frontend

```bash
cd frontend
streamlit run app.py
```

* **Backend:** [http://localhost:8000](http://localhost:8000)
* **Frontend:** [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker Deployment

### Build & Run (Both Services)

```bash
docker-compose up --build
```

* Backend → port 8000
* Frontend → port 8501

---

## 🚀 Deploy on Render

1. Push repo to GitHub
2. Connect to [Render](https://render.com)
3. Add env vars in Render Dashboard
4. Render will build & deploy via GitHub Actions

---

## 📊 Dashboard Metrics (via Supabase)

* Total queries processed
* Avg response time
* Top documents
* Usage trends
* Accuracy rate

---

## 🌱 Future Enhancements

* Add LangFuse observability layer
* Support multi-document search
* Add Supabase Auth for login
* Add exportable analytics reports
* Fine-tune Gemini model on custom dataset

---

## 👨‍💻 Author

**Awanish Kumar**
💼 AI Engineer @ Genpact | Ex-HCL | GenAI | RAG | LLM | MLOps
📧 [Email](mailto:awanish@example.com) • 🌐 [LinkedIn](https://linkedin.com/in/awanish) • 🧑‍💻 [GitHub](https://github.com/awanish)

---

## 🪪 License

Licensed under the **MIT License** — free for personal and educational use.

---

## ⭐ Support the Project

If you liked this project:

* ⭐ Star the repo on GitHub
* 🧠 Fork it and extend it
* 💬 Share feedback or open issues

> *Built with 💙 using Gemini, Pinecone, Supabase, LangChain, FastAPI & Streamlit*


