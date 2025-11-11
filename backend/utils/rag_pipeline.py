"""
RAG Pipeline:
1️⃣ Extract → 2️⃣ Chunk → 3️⃣ Embed → 4️⃣ Store → 5️⃣ Retrieve → 6️⃣ Generate Answer → 7️⃣ Log to Supabase
"""

import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone
from supabase import create_client, Client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google.genai import types

# Load environment variables
load_dotenv()

# === ENV ===
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
EMBED_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")
CHAT_MODEL = os.getenv("GEMINI_NLP_MODEL")
CHUNK_SIZE = 100
CHUNK_OVERLAP = 20

# === Initialize clients ===
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- 1️⃣ Extract text (placeholder for PDF text) ---
def extract_text_from_pdf(pdf_text: str):
    return pdf_text  # assume already extracted by pdf_loader

# --- 2️⃣ Chunk Text ---
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    splitted_text = splitter.split_text(text)
    print(len(splitted_text))
    return splitted_text

# --- 3️⃣ Create & Upload Embeddings ---
def store_embeddings_in_pinecone(chunks, doc_id):
    for i, chunk in enumerate(chunks):
        emb = genai_client.models.embed_content(
            model=EMBED_MODEL, 
            contents=chunk,
            config=types.EmbedContentConfig(output_dimensionality=1536)
        ).embeddings[0].values
        index.upsert(vectors=[(f"{doc_id}_chunk{i}", emb, {"text": chunk})])
    print(f"✅ Stored {len(chunks)} chunks for {doc_id}")

# --- 4️⃣ Retrieve Top-k ---
def retrieve_from_pinecone(query, top_k=3):
    query_emb = genai_client.models.embed_content(
        model=EMBED_MODEL, 
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    ).embeddings[0].values
    results = index.query(vector=query_emb, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]

# --- 5️⃣ Generate Final Answer ---
def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)
    print("Context: ", context)
    prompt = f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
    response = genai_client.models.generate_content(model=CHAT_MODEL, contents=prompt)
    return response.text.strip()

# --- 6️⃣ Log to Supabase ---
def log_query_to_supabase(session_id, question, answer, source_docs):
    supabase.table("user_queries").insert(
        {
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "source_docs": source_docs
        }
    ).execute()

# --- 7️⃣ Main RAG Function ---
def rag_pipeline_run(pdf_text, question, session_id="session_1"):
    # 1. Chunk
    chunks = chunk_text(pdf_text)

    # 2. Store Embeddings
    store_embeddings_in_pinecone(chunks, session_id)

    # 3. Retrieve
    relevant_chunks = retrieve_from_pinecone(question)

    # 4. Generate Answer
    answer = generate_answer(question, relevant_chunks)

    # 5. Log
    source_docs = "\n\n".join(relevant_chunks)
    log_query_to_supabase(session_id, question, answer, source_docs)

    print("✅ Answer:", answer)
    return answer

pdf_text = """What is Machine Learning?
    As all of us is very much clear about the leaning concept of humans, they learn from their past experiences. 
    But can we expect the same from computers or any machine to learn itself from the given raw data and past 
    experiences? Thereby the concept of machine learning came into existence.

    Machine learning is a subset of artificial intelligence that learns through the raw data and past experiences 
    without being actually programmed explicitly, to give some sense to the data exactly in same manner as humans can 
    do. In other words we can say that ML is a field of Computer Science that deals in extracting out some sensible 
    data on being processed by some ML algorithms. Machine learning was introduced by Arthur Samuel in 1959.
    
    “Machine learning uses statistical tools on data to output a predicted value. It is an application of artificial 
    intelligence that provides the system with the ability to learn and improve from experience without being explicitly 
    programmed automatically”.

    What is the need of Machine Learning?
    Nowadays, humans have become more advanced and work quite intelligently, especially the way they handle difficult 
    problems and solve them. While on the other hand there is AI which is still undergrowth and has not beaten the human 
    intelligence yet. And so, machine learning is needed for decision making on the basis of some raw data in an 
    efficient manner at a large scale.

    As of now, the developers are much more into developing technologies like artificial intelligence, deep learning, 
    and machine learning to extract some information from the given data and performs different algorithm to solve some 
    actual real-world problems especially on a huge scale working as a helping hand to the organization. It can also be 
    known as data-driven decision making. The decision making does not require any programming logic, rather the driven 
    data can be used itself. And for that, it does require human intelligence. Also, the human itself is not enough to 
    solve the real-world problem at a huge scale. So this is when machine learning is needed. As more the data, better 
    the model and higher would be its accuracy.
    """
question = "What is the use of datascience?"
print(rag_pipeline_run(pdf_text, question))