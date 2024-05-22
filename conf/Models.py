from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from src import GOOGLE_API_KEY


text_model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
    convert_system_message_to_human=True,
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=GOOGLE_API_KEY
)
# Selecting the first and only text generation model available in palm

memory = ConversationBufferMemory(ai_prefix="AI", llm=text_model)
