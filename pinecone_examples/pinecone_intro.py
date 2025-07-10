import os

from dotenv import load_dotenv
from pinecone import Pinecone
load_dotenv()

pinecone_key = os.getenv("PINECONE_API")
pc = Pinecone(api_key=pinecone_key)


# Create Index

# pc.create_index(
#     name="quickstart",
#     dimension=8,
#     metric="euclidean",
#     spec=ServerlessSpec(cloud="aws", region="us-east-1"),
# )

index = pc.Index("quickstart")

index.upsert(
    vectors=[
        {
            "id": "A",
            "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            "metadata": {"genre": "comedy", "year": 2020},
        },
        {
            "id": "B",
            "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
            "metadata": {"genre": "documentary", "year": 2019},
        },
        {
            "id": "C",
            "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            "metadata": {"genre": "comedy", "year": 2019},
        },
        {
            "id": "D",
            "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
            "metadata": {"genre": "drama"},
        },
    ],
    namespace="example-namespace",
)

res = index.query(
    namespace="example-namespace",
    vector=[0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
    top_k=2,
    include_metadata=True,
    include_values=False,
    filter={"gener": {"$eq": "drama"}},
)
print(res)
print(res.matches)
