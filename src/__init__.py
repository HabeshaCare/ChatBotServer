import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("API_KEY")
FILE_PATH = os.getenv("FILE_PATH")
