from tqdm.auto import tqdm
import time
from typing import List
from conf.Models import embedding_model
from src import PINECONE_API_KEY, pc
from utils.HelperFunctions import check_token, generate_random_string
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeApiException

from utils.InputUtils import prepare_embedding, prepare_query
from flask import jsonify


def get_or_create_index(name: str):
    try:
        index = pc.Index(name)
        return index
    except PineconeApiException as e:
        if e.status == 404:
            print("Index not found, creating new index...")
            index = create_pinecone_index(name)
            return index
        else:
            print(e.body)
            raise e


def get_vector_with_doctor_id(doctor_id: str, index):
    result = index.query(
        vector=[0.1 for _ in range(768)],
        filter={"doctor_id": {"$eq": doctor_id}},
        include_metadata=True,
        include_values=False,
        top_k=1,
    )
    result = result.get("matches")
    return result


def delete_from_index(doctor_id: str, index) -> None:
    result = get_vector_with_doctor_id(doctor_id, index)

    if len(result) != 0:
        index.delete(ids=[r.get("id") for r in result])

    return len(result) != 0


def update_from_index(doctor_id: str, updated_document, index) -> None:
    result = get_vector_with_doctor_id(doctor_id, index)
    if len(result) != 0:
        updated_document = prepare_embedding(updated_document)
        embedding = embed_function([updated_document])
        index.upsert(
            vectors=[
                {
                    "id": result[0].get("id"),
                    "values": embedding[0],
                    "metadata": {"doctor_id": doctor_id, "Updated": True},
                }
            ]
        )

    return len(result) != 0


# Function to create embeddings for given documents using palm's embedding model
def embed_function(documents: List[str]):
    # Embed the documents using any supported method
    return embedding_model.embed_documents(documents)


# Function to create a Pinecone index to store the embeddings.
def create_pinecone_index(name: str, documents: List[str] = None):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    pc.create_index(
        name=name,
        metric="cosine",
        dimension=768,
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    # wait for index to be initialized
    while not pc.describe_index(name).status["ready"]:
        time.sleep(1)

    if documents:
        add_to_index(documents, index)

    index = pc.Index(name)
    return index


# Function to add to the Pinecone index after the index is set up given the documents array and index
def add_to_index(documents, index):
    doctor = documents[0]
    doctor = prepare_embedding(json_data=doctor)
    embeddings = embed_function([doctor])
    annotated_documents = [
        {
            "id": generate_random_string(),
            "values": embedding,
            "metadata": {"doctor_id": document.get("id")},
        }
        for embedding, document in zip(embeddings, documents)
    ]
    insert_success = True
    for document in tqdm(annotated_documents):
        result = index.upsert(vectors=[document])
        insert_success &= len(result) != 0

    return insert_success


def empty_index(index):
    collection = index.delete(delete_all=True)
    return len(collection) == 0


# Function to query the index with a question and get the top 3 documents and filters out any irrelevant ones
def get_relevant_results(query: str, index, metadata=True, results=3):
    embedding_query = embedding_model.embed_query(query)

    results = index.query(
        vector=embedding_query,
        top_k=results,
        include_metadata=metadata,
        include_values=False,
    )

    results = results.get("matches")
    results = [result for result in results if result["score"] > 0.5]

    return results


def search_doctor(query: str):
    try:
        index = pc.Index("doctors")
        query = prepare_query(query)

        print(query)

        results = get_relevant_results(query, index, metadata=True, results=20)
        formatted_results = [
            {
                "id": res.get("metadata", {}).get("doctor_id", {}),
                "score": res.get("score", 0.0),
            }
            for res in results
        ]

        response = {
            "success": True,
            "statusCode": 200,
            "data": formatted_results,
            "errors": [],
            "message": f"Found {len(formatted_results)} matching doctors",
        }
        return jsonify(response), 200
    except Exception as e:
        response = {
            "success": False,
            "statusCode": 500,
            "data": None,
            "errors": [str(e)],
            "message": "Searching for doctors failed",
        }
        return jsonify(response), 500


def create_doctor(doctor):
    try:
        index = pc.Index("doctors")
        success = add_to_index([doctor], index)

        response = {
            "success": success,
            "statusCode": 200,
            "data": None,
            "errors": [],
            "message": "Adding doctor success: " + str(success),
        }

        return jsonify(response), 200

    except ValueError as e:
        response = {
            "success": False,
            "statusCode": 400,
            "data": None,
            "errors": [str(e)],
            "message": "Please make sure the doctor data is provided correctly",
        }
    except Exception as e:
        response = {
            "success": False,
            "statusCode": 500,
            "data": None,
            "errors": [str(e)],
            "message": "Something went wrong while adding doctor",
        }

        return jsonify(response), 500


def update_doctor(doctor_id, updated_doctor):
    try:
        index = pc.Index("doctors")
        updated = update_from_index(doctor_id, updated_doctor, index)
        response = {
            "success": updated,
            "statusCode": 201,
            "message": "Updated doctor success: " + str(updated),
            "errors": [],
            "data": None,
        }
        return jsonify(response), 201

    except Exception as e:
        response = {
            "success": False,
            "data": None,
            "errors": [str(e)],
            "message": "something went wrong while updating doctor",
            "statusCode": 500,
        }
        return jsonify(response), 500


def delete_doctor(doctor_id):
    try:
        index = pc.Index("doctors")
        deleted = delete_from_index(doctor_id, index)

        response = {
            "success": deleted,
            "data": None,
            "errors": [],
            "message": "Deleting doctor success: " + str(deleted),
            "statusCode": 201,
        }

        return jsonify(response), 201

    except Exception as e:
        response = {
            "success": False,
            "data": None,
            "errors": [str(e)],
            "message": "Something went wrong while deleting doctor",
            "statusCode": 500,
        }

        return jsonify(response), 500


def reset_database():
    try:
        index = pc.Index("doctors")
        reset = empty_index(index)
        response = {
            "success": reset,
            "data": None,
            "message": "Database reset: " + str(reset),
            "errors": [],
            "statusCode": 201,
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            "success": False,
            "data": None,
            "message": "Something went wrong while resetting the database",
            "errors": [],
            "statusCode": 500,
        }

        return jsonify(response), 500
