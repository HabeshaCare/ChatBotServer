from typing import Any, Dict, List
from conf.Models import text_model
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json


def prepare_embedding(json_data: Dict[str, Any]) -> str:

    if "id" not in json_data or json_data.get("id") == None:
        raise ValueError("Id attribute is required")

    description = json_data.get("description", "")
    specialization = json_data.get("specialization", "")
    years_of_experience = json_data.get("yearOfExperience", "")
    name = json_data.get("fullname", "")
    gender = json_data.get("gender", "")

    embedding_string = f""" Description: {description} 
                            Specialization: {specialization}
                            Experience in Years: {years_of_experience}
                            Fullname: {name}
                            Gender: {gender}"""

    if embedding_string == "":
        raise ValueError("No data to generate embedding from.")

    return embedding_string


def prepare_query(query: str) -> str:
    template = """
        Extract the fields and return a string strictly following the following format from the following input query and output it in the following format. You shouldn't output anything else except for the fields in specified format. If you couldn't' find the felid, leave it blank and don't put any text as it's value just leave the key before it and end it with the ':'. 
        Text: {query}
        Format: ``` Description: 'This is a catch all field for anything that didn't match in the rest and if you think it is relevant to find a doctor' 
                    Specialization: 'The doctors specialization' 
                    Experience in Years: 'Years of experience in number '
                    Fullname: 'Full name of the doctor' 
                    Gender: 'Gender of the doctor or try to guess based on the pronouns used in the query' ```
    """

    prompt = PromptTemplate.from_template(
        template,
        partial_variables={"query": query},
    )

    conversation = LLMChain(prompt=prompt, llm=text_model, verbose=False)
    answer = conversation.predict(input=query)
    return answer


def prepare_patient_history(json_data: List[Dict[str, Any]]) -> str:
    if not isinstance(json_data, list):
        raise ValueError("Input data must be a list of JSON objects")

    formatted_data = []
    for item in json_data:
        if not isinstance(item, dict):
            raise ValueError("Each item in the list must be a JSON object")
        formatted_data.append(json.dumps(item))

    result = "\n".join(formatted_data)

    return result
