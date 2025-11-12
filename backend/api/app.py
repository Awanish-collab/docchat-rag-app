from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.store_embeddings import store_embeddings_in_pinecone
from utils.query_rag import rag_query_run
from utils.common import supabase
from utils.pdf_reader import extract_text_pypdf2, extract_text_from_upload

app = FastAPI(title="DocChat RAG API")

# --- Allow frontend access ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "✅ DocChat RAG API running successfully"}

# --- 1️⃣ Upload PDF & store embeddings ---
@app.post("/upload")
async def upload_document(file: UploadFile, session_id: str = Form(...)):
    """
    Accepts a PDF upload, extracts text, chunks, embeds, and stores in Pinecone.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Extract text from uploaded file
    pdf_text = extract_text_from_upload(file)
    
    if not pdf_text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")
    
    # Store embeddings
    store_embeddings_in_pinecone(pdf_text, session_id)
    
    return {
        "status": "success", 
        "session_id": session_id, 
        "message": "Document embeddings stored.",
        "text_length": len(pdf_text)
    }

# --- 2️⃣ Ask a query ---
@app.post("/query")
async def ask_query(session_id: str = Form(...), query: str = Form(...)):
    """
    Takes a question, retrieves relevant context from Pinecone, generates answer using Gemini,
    and logs the query-answer pair to Supabase.
    """
    answer = rag_query_run(query, session_id)
    return {"session_id": session_id, "question": query, "answer": answer}

# --- 3️⃣ Fetch user query history ---
@app.get("/history/{session_id}")
def get_history(session_id: str):
    data = supabase.table("user_queries").select("*").eq("session_id", session_id).execute()
    return {"session_id": session_id, "history": data.data}
