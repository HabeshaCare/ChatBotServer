import os
from dotenv import load_dotenv
import google.generativeai as palm
from langchain.llms import GooglePalm
from langchain.memory import ConversationBufferMemory


load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
shared_secret = os.environ.get("LLM_SERVER_SECRET")
llm_url = os.environ.get("LLM_URL")

palm.configure(api_key=api_key)

# Selecting the first and only text generation model available in palm
text_model = GooglePalm(temperature=0.0, google_api_key=api_key)

memory = ConversationBufferMemory(
    ai_prefix="AI",
    llm=text_model
)
