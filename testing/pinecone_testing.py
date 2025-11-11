from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

print("Pinecone API Key: ", os.getenv("PINECONE_API_KEY1"))
print("Pinecone Index Name: ", os.getenv("PINECONE_INDEX_NAME"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY1"))
print("PC ", pc)
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

stats = index.describe_index_stats()
print("✅ Pinecone index connected successfully!")
print(stats)
