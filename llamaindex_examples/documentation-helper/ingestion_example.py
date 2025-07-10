from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from llama_index.core import (
    VectorStoreIndex,
)
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.settings import Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers.type import ResponseMode

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.prompts import PromptTemplate


# llm = Ollama("llama3.2", temperature=0.0, request_timeout=120)
llm = llm = Ollama("gemma3:4b")
# llm = Ollama("deepseek-r1:7b", request_timeout=300)
# llm = Ollama("granite3.3:8b", request_timeout=60)

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5", embed_batch_size=100, device="cuda"
)
Settings.llm = llm
Settings.embed_model = embed_model


load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API"))
pc_index = pc.Index("llamaindex-helper-documentation")
vector_store = PineconeVectorStore(pc_index)
vector_index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store, embed_model=Settings.embed_model
)


prompt = PromptTemplate(
    "You are a helpful assistant. Use the context below to answer the question.\n\n"
    "Answer the question directly. If the context does not contain the answer, IGNORE IT and use your own knowledge."
    "Context:\n{context_str}\n\n"
    "Question: {query_str}\n\n"
    "Answer:"
)

query_engine = vector_index.as_query_engine(
    similarity_top_k=20,
    response_mode="refine",
    text_qa_template=prompt,
)

# resp = query_engine.query("Which is the current version of llama-index-core?")
resp = query_engine.query("Which is the current version of llama-index-core?")
print("🏷️ Answer:", resp)
resp = query_engine.query("This is other topic, which is the capital of colombia")
print("🏷️ Answer:", resp)
