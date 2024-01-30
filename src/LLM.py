# This module contains functions related to LLM and Tranlation. AI in general.
import re
from langchain.prompts.prompt import PromptTemplate
from utils.HelperFunctions import check_token, parse_response
from conf.Models import text_model, memory
from langchain.chains import LLMChain


# Function to return a structured format of the prompt
def make_prompt() -> str:
    DEFAULT_TEMPLATE = """
         You are  Hakime a health assistant for patients, especially on stroke.
         You will be given a question below, and you are not allowed to answer a question that is not related to health and medicine
         if the question is greeting you are alowed to answer 
         if you are asked who you are or what you say that you are  NuroGen a health assistant
         just tell the user that you cannot answer a question not related to health . 
         If the question is related to health, give a response.
Previous Conversation: {history}
Human: {input}
"""
    PROMPT = PromptTemplate.from_template(DEFAULT_TEMPLATE)

    return PROMPT


def generate(
    query: str,
    model=text_model,
):
    prompt = make_prompt()
    conversation = LLMChain(
        prompt=prompt, llm=model, memory=memory, verbose=False
    )
    try:
        history = memory.load_memory_variables({}).get("history")

        # To add additional layer of protection against token limit exceeding
        if history and not check_token(history):
            print(f"token length: {len(history) / 4}")
            memory.chat_memory.clear()
            print("Cleared chat memory due to large token number")
        answer = conversation.predict(input=query)
        print("\033[94m" + answer + "\033[0m")

        # Extract the response
        aiAnswer = parse_response(answer)
        validAnswer = aiAnswer and (not aiAnswer.isspace())

        answer = aiAnswer if validAnswer else answer
        return answer, ""
    except Exception as e:
        print(e)
        return (
            "Hakime can't answer your question since there isn't enough context. Please try rephrasing your quesiton or ask another one!",
            "",
        )


def loadMessagesToMemory(messages) -> bool:
    for message in messages:
        if ("content" in message) and message["content"]:
            if message["type"] == "chatbot":
                memory.chat_memory.add_ai_message(message["content"])
            else:
                memory.chat_memory.add_user_message(message["content"])
    return len(memory.chat_memory.messages) > 0