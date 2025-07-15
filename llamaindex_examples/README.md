This is like LangChain in the part of vector db, please refer to [Vector DB](../chromadb_exampels/README.md)

What is RAG?
RAG stands for Retrieval Augmented Generation, which is a framework used to answer questions over unstructured documents using Large Language Models (LLMs). The primary goal of RAG is to retrieve relevant information from the document and then generate a response based on that retrieved information.

How LlamaIndex Handles RAG
LlamaIndex provides simple-to-advanced techniques for Retrieval Augmented Generation. You can choose to use either their prebuilt RAG abstractions (e.g., query engines) or build custom RAG workflows.

Simple Queries
The simplest queries involve either semantic search or summarization.

Semantic Search
Semantic search involves finding information in a document that matches the query terms and/or semantic intent. This is typically executed with simple vector retrieval (top-k).

Example:
```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Sample data
data = {
    'text': ['This is a sample text.', 'Another sample text.', 'Text for summarization.']
}

df = pd.DataFrame(data)

# Define query terms
query_terms = ['sample', 'text']

# Calculate similarity scores
similarity_scores = cosine_similarity(df['text'], query_terms)

# Get top-k results
top_k_results = df.loc[similarity_scores.argsort()[:3]]

print(top_k_results)
```


Summarization
Summarization involves condensing a large amount of data into a short summary relevant to the current question.

Example:
```python
import pandas as pd

# Sample data
data = {
    'text': ['This is a sample text.', 'Another sample text.', 'Text for summarization.']
}

df = pd.DataFrame(data)

# Define summarization threshold (e.g., 100 words)
threshold = 100

# Calculate summary length
summary_length = df['text'].str.len().max()

# Truncate or summarize the text based on the threshold
if summary_length > threshold:
    df['summary'] = df['text'].apply(lambda x: x[:threshold])
else:
    df['summary'] = df['text']

print(df)
```

Advanced RAG Workflows
LlamaIndex also provides advanced techniques for building custom RAG workflows, such as Corrective RAG.

Example (using LlamaIndex's workflow API):
```python
import llama_index as li

# Define the workflow
workflow = li.Workflow(
    query_engine=li.QueryEngine('vector_retrieval'),
    chat_engine=li.ChatEngine('text_generation')
)

# Add a corrective step to the workflow
workflow.add_corrective_step(li.CorrectiveStep(
    retriever=li.Retriever('vector_retrieval'),
    generator=li.Generator('text_generation')
))

# Run the workflow
results = workflow.run(query_terms=['sample', 'text'])
print(results)
```

Note: This is just a brief overview of how LlamaIndex handles RAG. For more information, please refer to their official documentation and guides.
### Data connectors
The way that llamaindex handle the connection to third parties applications, own data sources or databases.

LlamaIndex provides a variety of data connectors that allow you to easily ingest data from different sources into your application. These connectors are designed to be flexible and extensible, making it easy to add new connectors as needed.

Existing Data Connectors
Some of the existing data connectors in LlamaIndex include:

- Google Docs Reader: Ingests data from Google Docs documents.
- Amazon S3 Reader: Ingests data from Amazon S3 buckets.
- Microsoft OneDrive Reader: Ingests data from Microsoft OneDrive files.
- Local File Reader: Ingests data from local files on your machine.
- Example: Using the Google Docs Reader
Here's an example of how to use the Google Docs Reader in Python:
```python

import llama_index as li

# Create a new instance of the Google Docs Reader
reader = li.GoogleDocsReader(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirect_uri='YOUR_REDIRECT_URI'
)

# Load data from a specific document ID
document_ids = ['DOCUMENT_ID_1', 'DOCUMENT_ID_2']
documents = reader.load_data(document_ids=document_ids)

# Print the loaded documents
for doc in documents:
    print(doc['text'])
```

Note: You'll need to replace YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, and YOUR_REDIRECT_URI with your actual Google OAuth credentials.

Adding a Custom Data Connector
If you want to add a custom data connector, you can create a new class that inherits from the Reader abstract base class. Here's an example of how to do this:
```python
import llama_index as li

class CustomDataConnector(li.Reader):
    def __init__(self, **kwargs):
        # Initialize your custom connector here
        pass

    def load_data(self, document_ids):
        # Load data from your source here
        pass

# Create an instance of the custom connector
connector = CustomDataConnector()

# Use the connector to load data
document_ids = ['DOCUMENT_ID_1', 'DOCUMENT_ID_2']
documents = connector.load_data(document_ids)

# Print the loaded documents
for doc in documents:
    print(doc['text'])
```

## Agents
Uses LLMs as reasoning engine and execute non deterministic sequence of actions ("tools")
### Uses cases
- Search
- APIS
  Databases
- Calculators
- Run code


>[!TIP]
>```python
>from llama_index.llms.ollama import Ollama
>from llama_index.core.agent import ReActAgent
>from llama_index.core.tools import FunctionTool
>
>
>llm = Ollama("llama3.2")
>
>def write_haiku(topic: str)->str:
>    """Writes a haiku about a given topic"""
>    return llm.complete(f"Write me a haiku about {topic}").text
>
>def count_characteres(text:str)-> int:
>    """Count the characteres in a text"""
>    return len(text)
>
>if __name__ == "__main__":
>    tool1 = FunctionTool.from_defaults(fn=write_haiku, name="write_haiku")
>    tool2 = FunctionTool.from_defaults(fn=count_characteres, name="count_characteres")
>    agent = ReActAgent.from_tools(tools=[tool1, tool2], llm=llm, verbose=True)
>
>    res = agent.query("Write me a haiku about tennis and count the characteres in it")
>    print(res)
>```

