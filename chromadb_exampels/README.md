What are the vector DB?

A vector Database encodes information as vectors in a multi-dimensional space to perform high-efficient based on similarity.

## How is the data in the world?

The data is 80% or more is unstructured.
- PDF
- Images
- Audio
- Etc ...


Vector db is the only one that can handle this type of data.

1. Efficient representation of complex data.
- Dimensionality  - representing data in high dimensional space
- Uniformity - data can be converted into uniform format (numerical vectors)

2. Enabling Similarity Search
3. Leveraging Machine Learning Models
4. optimizing Performance and Scalability
5. Improving User Experience

## Traditional databases

- Structured data: predefined columns and rows.
- Schema based; Database structure must be defined before hand
- Data manipulation and querying: Manipulation through SQL
- ACID complain: Atomic, Consistency, Isolation, Durability
- Indexing: to speed up data retrieval


### Limitations
- Scalability: hard to deal with complex queries across large tables
- Flexibility: changing DB's schema can be disruptive
- Handling Unstructured Data: not well suited for unstructured data (audio, pdf, etc ...)

## Transform unstructured data into vectors  - Deep dive
Text with similar content and meaning have similar vectors.



### Vector database (vectorstore)

The query is converted to an embedded and find the more similar vector in the db. Cosine similarity.

**Embeddings vs Vectors**
Are essentially the same thing, but change in definition.

- *Vector*: Mathematical representation of data in an n-dimensional space (each dimension == a feature of the data)
	- Are generic and used in a wide range of applications
- *Embedding*: A specific type of vector used in Machine learning and Artificial Intelligence.
	- Map raw data into a vector space (**preserves** semantic relationship - **meaning**)

```ad-summary
Embeddings are **vectos**, but not all vectors are embeddings.
```

### Advantages
- **Data representation as Vectors**: Vector is vectorized which brings lots of benefits for searching
- **Similarity Search**: Finding data points closest to a given vector query
- **Efficiency in High-Dimensional Searches**: Use specialized indexing structures are highly optimized.
- **Handling Unstructured Data**
- **Schema-Less Design**

### Uses cases
1. Image Retrieval & Similarity Search.
2. Recommendation systems.
3. Natural Language Processing (NLP).
4. Fraud detection & Bioinformatics


## Vectors DB

- Milvus
- Pinecone
- Faiss (Facebook AI Similarity Search)
- Weaviate
- Annoy (Approximate Nearest Neighbors Oh Yeah)
- Chroma - AI  Native & Open Source



### ChromaDB

Simple chromadb example
```python
import chromadb

chroma_client = chromadb.Client()

collection_name = "test_collection"

collection = chroma_client.get_or_create_collection(name=collection_name)

documents = [
    {"id": "doc1", "text": "Hello, world!"},
    {"id": "doc2", "text": "How are you today?"},
    {"id": "doc3", "text": "Goodbye, see you later!"},
]

for doc in documents:
    collection.upsert(ids=doc["id"], documents=doc["text"])

query = "Hello, world!"

results = collection.query(
    query_texts=[query],
    n_results=3,
)

print(results)

```

#### Embedding functions
```python
from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()

name = "Paulo"

emb = default_ef(name)
print(emb)
```

If you want to change the embedding function for the collection, you can add the embedding function in the chroma client
```python
import chromadb
from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()

chroma_client = chromadb.Client()

collection_name = "test_collection"

collection = chroma_client.get_or_create_collection(name=collection_name, embedding_function=default_ef)
```

#### Persistence data
Only need to change the client for PersistenceClient
```python
...
croma_client = chromadb.PersistentClient(path="./db/chroma_persistence")
...
```

## Metrics and Data structure
**Metrics**:
- Latency: time it takes to complete a query
- Throughput: # of queries that can be processed per unit of time
- Precision and Recall: evaluation of accuracy of the search result
- Memory usage
- Scalability

**Data structures**:
- Inverted indexes
- K-d Trees
- Hierarchical Navigable Small World (HNSW) Graphs
- Locality-Sensitive Hashing (LSH)
- Priority Queues

# Building Vector database - Hand-On
Similarity influenced by:
- Direction
- Magnitude
- Relative position

## Common measures of vector similarity
- Cosine Similarity
	- Magnitude (distance) doesn't matter
	- The angle (cosine) is what matters
		- Higher value means similar
		- Value btwn -1 and 1
	- Best Uses:
		- Topic modeling
		- Document similarity
		- Collaborative filtering
 $$
	Cosine Similarity(A,B) = \frac{A\cdot{B}}{||A||\quad ||B||}
$$

- Euclidean Distance - L2 Norm
	- Best Uses:
		- Clustering Analysis
		- Anomaly & fraud detection
$$
Euclidean distance (A,B) = \sqrt{\sum\limits_{i=1}^n(A_i - B_i)^2}
$$
- Dot Product
	- Best Use:
		- Image retrieval & matching
		- Music Recommendation
$$
Dot Product(A,B) = A\cdot{B} = \sum\limits_{i=1}^nA_iB_i
$$

# Which to use?
1. Project Requirements
	1. Scalability
	2. Performance needs
	3. Data type
2. Ease of use and Integration
	1. Developer experience
	2. Community support
3. Feature Set
	1. Customization and flexibility
4. Cost and Infratructure
5. Security and Compliance

## Criterias
- Data type and volume
	- Text, images or Audio: Weaviate or Chroma
	- Scalability: Vertical and Horizontal - Pinecone and Milvus
- Query Performance and latency:
	- Latency requirements - low latency applications - Pinecone
- Accuracy and Precision:
	- Metric support: Support similarity metrics
	- Tunning capabilities
- Ease of integration and Use
	- API and SDK Libraries
	- Documentation and Community
- Cost consideration
- Security and Compliance
- Vendor Stability and Support
