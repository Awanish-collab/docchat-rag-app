from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

# pip install -q -U google-genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?",
        config=types.EmbedContentConfig(output_dimensionality=1536)
        )

embed =  result.embeddings[0].values

print(len(embed))