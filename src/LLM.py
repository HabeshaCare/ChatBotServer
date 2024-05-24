# This module contains functions related to LLM and Translation. AI in general.
import re
from typing import Any, Dict, List
from langchain.prompts import PromptTemplate
from utils.HelperFunctions import check_token, parse_response
from conf.Models import text_model, memory
from langchain.chains import LLMChain

from utils.InputUtils import prepare_patient_history


# Function to return a structured format of the prompt
def make_prompt(patient_history: List[Dict[str, Any]] = []) -> str:
    DEFAULT_TEMPLATE = """
         You are  Hakime a health assistant for patients and doctors.
         You will be given a question below, and you are not allowed to answer a question that is not related to health, medicine or question related to the patient data provided below. Here is a general rules you can follow while answering any question:
         1. If the question is greeting or any casual question, you are allowed to answer.
         2. If you are asked who you are say that you are 'Hakime' a health assistant chat bot.
         3. If the question is related to health, give a response.
         4. If the question is related to the provided patient data and if the provided data is patient data you are allowed to answer.
         5. Here is additional instruction to consider only if a patient's data is provided:
         ```You can also answer questions that are about a patient data if the context is provided below. If you are given a patient's medical data, you should also try to answer the question based on the data provided. If the data is irrelevant to the question being asked, you can ignore it. However, if the data is related but it doesn't have enough information to answer the question, you should by no means answer the question based on assumptions, instead you should just say that you are sorry and there isn't enough information to answer that question.```
Previous Conversation: {history}
Human: {input}
Patient History: {patient_history}
"""
    formatted_patient_history = prepare_patient_history(patient_history)
    PROMPT = PromptTemplate.from_template(
        DEFAULT_TEMPLATE,
        partial_variables={"patient_history": formatted_patient_history},
    )

    return PROMPT


def generate(
    query: str,
    patient_history: List[Dict[str, Any]],
    model=text_model,
):
    prompt = make_prompt(patient_history)
    conversation = LLMChain(prompt=prompt, llm=model, memory=memory, verbose=True)
    try:
        history = memory.load_memory_variables({}).get("history")
        # print(f"History: {history}")

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
            "Hakime can't answer your question since there isn't enough context. Please try rephrasing your question or ask another one!",
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
