import os
from typing import Any

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openapi_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openapi_key, model_name="text-embedding-3-small"
)

croma_client = chromadb.PersistentClient(path="./db/chroma_persistence")

collection = croma_client.get_or_create_collection(
    "document_qa_collection", embedding_function=openai_ef
)


def load_documents_from_directory(directory_path: str) -> list[dict[str, Any]]:
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(
                os.path.join(directory_path, filename),
            ) as file:
                documents.append({"id": filename, "text": file.read()})
    return documents


def split_test(text: str, chunk_size: int = 1000, chunk_overlap: int = 20) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks


directory_path = ""
documents = load_documents_from_directory(directory_path)

chunked_documents = []
for doc in documents:
    chunks = split_test(doc["text"])
    for i, chunk in enumerate(chunks):
        chunked_documents.append({"id": f"{doc['id']}"})


def get_openai_embedding(text: str) -> list[float]:
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


for doc in chunked_documents:
    doc["embedding"] = get_openai_embedding(doc["text"])

for doc in chunked_documents:
    collection.upsert(
        ids=[doc["id"]], documents=[doc["text"]], embeddings=[doc["embedding"]]
    )


# =================== Query ================================= #
def query_documents(question: str, n_results: int = 2):
    results = collection.query(query_texts=question, n_results=n_results)
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    return relevant_chunks


# =================== Chat ================================= #


def generat_response(question: str, relevant_chunk: list):
    context = "\n\n".join(relevant_chunk)
    prompt = (
        "You are an assitant for question-answering task. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you"
        "don't know. Use three sentences maximum and keep the answer concise"
        "\n\nContext:\n" + context + "\n\nQuestion:\n"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
    )

    return response


question = "Tell me about databricks acquisition of ai services"
relevant_chunks = query_documents(question)
answer = generat_response(question, relevant_chunks)
print(answer.content)
