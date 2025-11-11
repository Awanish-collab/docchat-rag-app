# backend/utils/common.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from supabase import create_client, Client
from google import genai

load_dotenv()

# Environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBED_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")
CHAT_MODEL = os.getenv("GEMINI_NLP_MODEL")

# Initialize clients
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai_client = genai.Client(api_key=GEMINI_API_KEY)
