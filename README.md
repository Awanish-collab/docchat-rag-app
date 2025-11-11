

# 🧠 DocChat RAG App (Gemini + Pinecone + Supabase + FastAPI + Streamlit)

🚀 An end-to-end **Retrieval-Augmented Generation (RAG)** application for interacting with PDFs using **Google Gemini**, **Pinecone**, and **Supabase**, built with **FastAPI (backend)** and **Streamlit (frontend)**.

---

## 📘 Overview

**DocChat RAG App** allows you to upload PDFs, ask natural language questions, and visualize analytics — all in real time.

### 🔧 The pipeline performs:

1. PDF extraction
2. Text chunking
3. Embedding generation
4. Storage in Pinecone
5. Query retrieval
6. Gemini LLM generation
7. Response + analytics logging

This system is fully **containerized (Docker)**, **deployable (Render / Hugging Face)**, and **free-tier compatible**.

---

## 🧱 System Architecture

📄 **PDF Upload**
⬇️
🧩 **LangChain Text Splitter (Chunking)**
⬇️
🧠 **Gemini Embedding Model → Pinecone (Vector DB)**
⬇️
❓ **Query → Retrieve Top-k Docs → Gemini Flash (LLM)**
⬇️
✅ **Answer + Context + Supabase (for logs)**
⬇️
📊 **Streamlit Dashboard (Analytics & Visualization)**

---

## ⚙️ Technology Stack

| Layer                      | Tool                             | Purpose                                       |
| -------------------------- | -------------------------------- | --------------------------------------------- |
| **LLM + Embeddings**       | Google Gemini (AI Studio)        | Text generation & vector embeddings           |
| **Vector Database**        | Pinecone                         | Store & retrieve embeddings efficiently       |
| **Relational Database**    | Supabase                         | Real-time logs & analytics storage            |
| **Backend API**            | FastAPI + Uvicorn                | Serve upload, query & analytics endpoints     |
| **Frontend UI**            | Streamlit                        | Chat interface + Upload + Analytics dashboard |
| **Visualization**          | Plotly / Altair                  | Display interactive charts                    |
| **Deployment**             | Docker + Render + GitHub Actions | Containerized CI/CD deployment                |
| **Environment Management** | dotenv                           | Secure API key management                     |
| **Optional Observability** | LangFuse                         | Track LLM performance (future)                |

---

## 📂 Folder Structure

```

docchat-rag-app/
│
├── 📁 backend/                                 # FastAPI backend service
│   ├── main.py                                 # FastAPI app entrypoint
│   ├── config.py                               # Load environment variables
│   ├── requirements.txt                        # Backend dependencies
│   │
│   ├── 📁 routes/                              # All API routes (organized by feature)
│   │   ├── upload_route.py                     # /upload endpoint
│   │   ├── query_route.py                      # /query endpoint
│   │   └── dashboard_route.py                  # /dashboard endpoint
│   │
│   ├── 📁 utils/                               # Helper modules
│   │   ├── pdf_loader.py                       # PDF text extraction
│   │   ├── text_splitter.py                    # Chunking via LangChain TextSplitter
│   │   ├── embedding.py                        # Gemini Embedding + Pinecone storage
│   │   ├── retriever.py                        # Pinecone retrieval (Top-k)
│   │   ├── llm_response.py                     # Gemini Flash LLM for final answers
│   │   ├── logger.py                           # Custom logging
│   │   └── validators.py                       # Input validation utils
│   │
│   ├── 📁 db/                                  # Database layer
│   │   ├── supabase_client.py                  # Supabase client for analytics
│   │   ├── schema.sql                          # SQL for initializing tables
│   │   └── models.py                           # Pydantic models for DB operations
│   │
│   ├── 📁 tests/                               # Backend testing
│   │   ├── test_api.py                         # Test upload & query routes
│   │   └── test_embeddings.py                  # Test embedding pipeline
│   │
│   ├── Dockerfile                              # Backend container config
│   ├── start.sh                                # Shell script for starting server
│   └── README.md
│
│
├── 📁 frontend/                                # Streamlit frontend dashboard
│   ├── app.py                                 # Main Streamlit entrypoint
│   ├── requirements.txt                       # Frontend dependencies
│   │
│   ├── 📁 components/
│   │   ├── upload_component.py                # PDF upload + processing
│   │   ├── chat_component.py                  # Chat interface (QA with LLM)
│   │   └── analytics_component.py             # Analytics dashboard (charts, trends)
│   │
│   ├── 📁 services/                           # For calling backend APIs
│   │   ├── api_client.py                      # Handles API requests to FastAPI
│   │   └── helpers.py                         # Common frontend utilities
│   │
│   ├── 📁 assets/                             # Static files
│   │   ├── logo.png
│   │   ├── styles.css
│   │   └── favicon.ico
│   │
│   ├── 📁 tests/
│   │   └── test_ui_components.py
│   │
│   ├── Dockerfile                             # Frontend container config
│   ├── start.sh                               # Frontend launch script
│   └── README.md
│
│
├── 📁 data/                                   # Data storage & logs
│   ├── uploads/                               # Raw uploaded PDFs
│   ├── chunks/                                # Chunked text files
│   ├── logs/                                  # Application logs
│   └── analytics/                             # Exported metrics
│
│
├── 📁 configs/                                # Configuration & credentials
│   ├── .env.example                           # Example environment file
│   ├── credentials_template.json              # Template for API keys
│   └── logging_config.yaml                    # Central logging configuration
│
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── deploy.yml                         # GitHub Actions for CI/CD (Render)
│
│
├── docker-compose.yml                         # Compose file for backend + frontend
├── .env                                       # Actual environment variables (not committed)
├── .gitignore                                 # Ignore sensitive & build files
├── LICENSE                                    # MIT License
├── README.md                                  # Project documentation
└── setup.md                                   # Developer setup instructions

```

---

## 🖥️ Frontend Screens

| Screen               | File                     | Purpose                          |
| -------------------- | ------------------------ | -------------------------------- |
| **Upload Screen**    | `upload_component.py`    | Upload PDFs & trigger embedding  |
| **Chat Screen**      | `chat_component.py`      | Ask questions, get LLM responses |
| **Analytics Screen** | `analytics_component.py` | Visualize usage analytics        |


---

## 🧩 Backend Endpoints

| Endpoint     | Method | Description                                                 |
| ------------ | ------ | ----------------------------------------------------------- |
| `/upload`    | POST   | Accepts a PDF, extracts text, chunks, and stores embeddings |
| `/query`     | POST   | Retrieves context and generates an answer                   |
| `/dashboard` | GET    | Fetches analytics from Supabase (query logs, usage stats)   |

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

### 4️⃣ Configure Environment

Create a `.env` file:

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

**Backend:** [http://localhost:8000](http://localhost:8000)
**Frontend:** [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker Deployment

### Build & Run Both Services

```bash
docker-compose up --build
```

* Backend → Port **8000**
* Frontend → Port **8501**

---

## 🚀 Deploy on Render

1. Push repo to GitHub
2. Connect repo to [Render](https://render.com)
3. Add environment variables
4. Build and deploy automatically via **GitHub Actions**

---

## 📊 Dashboard Metrics (via Supabase)

* Total queries processed
* Average response time
* Top documents
* Usage trends
* Accuracy rate

---

## 🌱 Future Enhancements

* Add **LangFuse** observability
* Support **multi-document search**
* Integrate **Supabase Auth** for login
* Add **exportable reports**
* Fine-tune Gemini model on custom data

---

## 👨‍💻 Author

**Awanish Kumar**
💼 AI Engineer @ Genpact | Ex-HCL | GenAI | RAG | LLM | MLOps
📧 [Email](mailto:awanish@example.com)
🌐 [LinkedIn](https://linkedin.com/in/awanish)
🧑‍💻 [GitHub](https://github.com/awanish)

---

## 🪪 License

Licensed under the **MIT License** — free for personal and educational use.

---

## ⭐ Support the Project

If you liked this project:

* ⭐ Star the repo on GitHub
* 🧠 Fork it and build your own version
* 💬 Share feedback or raise an issue

> *Built with 💙 using Python, Langchain, Gemini, Pinecone, Supabase, LangChain, FastAPI & Streamlit.*



