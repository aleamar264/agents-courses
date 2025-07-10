import chromadb
from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()
croma_client = chromadb.PersistentClient(path="./db/chroma_persistence")

collection = croma_client.get_or_create_collection(
    "my_story", embedding_function=default_ef
)


document = [
    {"id": "doc1", "text": "Hello, world!"},
    {"id": "doc2", "text": "How are you today?"},
    {"id": "doc3", "text": "Goodbye, see you later!"},
    {"id": "doc4", "text": "Microsoft is a technology company that develops software"},
]


for doc in document:
    collection.upsert(ids=doc["id"], documents=doc["text"])

query_text = "Age of the Earth"

results = collection.query(query_texts=[query_text], n_results=2)

for idx, document in enumerate(results["documents"][0]):
    doc_id = results["ids"][0][idx]
    distance = results["distances"][0][idx]
    print(
        f"For the query {query_text} \n We found similar document: {document} (ID: {doc_id}, Distance: {distance})"
    )
