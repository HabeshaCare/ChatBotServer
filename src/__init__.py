import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

GOOGLE_API_KEY = os.getenv("API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
FILE_PATH = os.getenv("FILE_PATH")

pc = Pinecone(api_key=PINECONE_API_KEY)
