from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("SUPABASE_URL"), "\n", os.getenv("SUPABASE_SERVICE_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

data = {
    "session_id": "test_session",
    "question": "What is RAG?",
    "answer": "Retrieval-Augmented Generation",
}
res = supabase.table("user_queries").insert(data).execute()

print("Inserted:", res)
