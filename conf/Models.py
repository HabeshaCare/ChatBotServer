import os
from dotenv import load_dotenv
import google.generativeai as palm
from langchain.llms import GooglePalm
from langchain.memory import ConversationTokenBufferMemory


load_dotenv()
api_key = os.environ.get("PALM_API_KEY")
shared_secret = os.environ.get("LLM_SERVER_SECRET")
llm_url = os.environ.get("LLM_URL")

palm.configure(api_key=api_key)

# Selecting the first and only text generation model available in palm
text_model = GooglePalm(temperature=0.0, google_api_key=api_key)

memory = ConversationTokenBufferMemory(
    ai_prefix="AI",
    llm=text_model,
    max_token_limit=4096,
)

embedding_model = [
    m for m in palm.list_models() if "embedText" in m.supported_generation_methods
][0]
