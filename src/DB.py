from tqdm.auto import tqdm
import time
from typing import List
from conf.Models import embedding_model
from src import PINECONE_API_KEY, pc
from utils.HelperFunctions import check_token, generate_random_string
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeApiException


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
    embeddings = embed_function(documents)
    annotated_documents = [
        {
            "id": generate_random_string(),
            "values": embedding,
            "metadata": {"doctor_id": document},
        }
        for embedding, document in zip(embeddings, documents)
    ]
    for document in tqdm(annotated_documents):
        index.upsert(vectors=[document])


def empty_index(index):
    index.delete(delete_all=True)


# Function to query the index with a question and get the top 3 documents and filters out any irrelevant ones
def get_relevant_results(query: str, index, metadata=False, results=3):
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
