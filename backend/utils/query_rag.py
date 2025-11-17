# backend/utils/query_rag.py
from google.genai import types
from .common import genai_client, index, supabase, EMBED_MODEL, CHAT_MODEL

# ---------------------- RETRIEVE -----------------------
def retrieve_from_pinecone(query, top_k=3):

    # ---- Generate embedding for query ----
    emb_response = genai_client.models.embed_content(
        model=EMBED_MODEL,
        contents=query,
        config=types.EmbedContentConfig(output_dimensionality=1536)
    )

    query_emb = emb_response.embeddings[0].values

    # ---- Estimate embedding tokens (since Gemini doesn't return usage) ----
    estimated_tokens = max(1, int(len(query) / 4))  # approx 4 chars = 1 token

    supabase.rpc("log_embedding_usage", {"token_count": estimated_tokens}).execute()


    # ---- Retrieve chunks ----
    results = index.query(vector=query_emb, top_k=top_k, include_metadata=True)

    contexts = []
    for match in results["matches"]:
        meta = match["metadata"]
        contexts.append({
            "chunk_text": meta.get("text"),
            "doc_id": meta.get("doc_id"),
            "file_name": meta.get("file_name"),
            "chunk_index": meta.get("chunk_index"),
            "score": match["score"]
        })

    return contexts


# ---------------------- GENERATE ANSWER -----------------------
def generate_answer(query, context_chunks):

    context_text = "\n\n".join([c["chunk_text"] for c in context_chunks])
    prompt = f"Context:\n{context_text}\n\nQuestion:\n{query}\n\nAnswer:"

    response = genai_client.models.generate_content(
        model=CHAT_MODEL,
        contents=[prompt]
    )

    answer = response.text.strip()

    usage = response.usage_metadata

    prompt_tokens = usage.prompt_token_count or 0
    completion_tokens = usage.candidates_token_count or 0
    total_tokens = usage.total_token_count or (prompt_tokens + completion_tokens)

    # ---------------- NLP ANALYTICS ----------------

    # 1️⃣ cumulative totals
    supabase.rpc("log_nlp_usage", {
        "prompt": prompt_tokens,
        "completion": completion_tokens,
        "total": total_tokens
    }).execute()

    # add cumulative tokens
    supabase.rpc("add_nlp_tokens", {"token_count": total_tokens}).execute()

    return answer, {
        "prompt": prompt_tokens,
        "completion": completion_tokens,
        "total": total_tokens
    }



# ---------------------- SUPABASE LOGGING -----------------------
def log_query_to_supabase(session_id, question, answer, contexts, tokens):

    supabase.table("user_queries").insert({
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "source_docs": contexts,
        "prompt_tokens": tokens["prompt"],
        "completion_tokens": tokens["completion"],
        "total_tokens": tokens["total"]
    }).execute()

    # --- NOW total_queries will increment correctly ---
    supabase.rpc("increment_queries").execute()


# ---------------------- MAIN RAG FN -----------------------
def rag_query_run(query, session_id="session_1"):

    retrieved = retrieve_from_pinecone(query)

    answer, tokens = generate_answer(query, retrieved)

    log_query_to_supabase(
        session_id=session_id,
        question=query,
        answer=answer,
        contexts=retrieved,
        tokens=tokens
    )

    print("Tokens used:", tokens)
    return answer
