# backend/utils/query_rag.py
from google.genai import types
from common import genai_client, index, supabase, EMBED_MODEL, CHAT_MODEL

def retrieve_from_pinecone(query, top_k=3):
    query_emb = genai_client.models.embed_content(
        model=EMBED_MODEL,
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    ).embeddings[0].values
    results = index.query(vector=query_emb, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]

def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
    response = genai_client.models.generate_content(model=CHAT_MODEL, contents=prompt)
    return response.text.strip()

def log_query_to_supabase(session_id, question, answer, source_docs):
    supabase.table("user_queries").insert({
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "source_docs": source_docs
    }).execute()

def rag_query_run(query, session_id="session_1"):
    chunks = retrieve_from_pinecone(query)
    answer = generate_answer(query, chunks)
    log_query_to_supabase(session_id, query, answer, "\n\n".join(chunks))
    print("✅ Answer:", answer)
    return answer

# Local test
if __name__ == "__main__":
    rag_query_run("Who is prime minister of india?")
