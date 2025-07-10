from dotenv import load_dotenv
import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser, MarkdownNodeParser
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import UnstructuredReader, MarkdownReader
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API"))

if __name__ == "__main__":
    # Load and chunk info
    dir_reader = SimpleDirectoryReader(
        input_dir="./llamaindex_examples/llamaindex-docs/docs",
        recursive=True,
        file_extractor={".md": UnstructuredReader()},
        required_exts=[".md"]
    )
    documents = dir_reader.load_data()
    node_parser = SimpleNodeParser.from_defaults(chunk_size=1000, chunk_overlap=100)
    # node_parser = MarkdownNodeParser()
    # nodes = node_parser.get_nodes_from_documents(documents=documents)

    # Configure Model
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-large-en-v1.5", embed_batch_size=100, device="cuda"
    )
    llm = Ollama("llama3.2", temperature=0.0, request_timeout=60)
    # ServiceContext is deprecated
    Settings.embed_model = embed_model
    Settings.node_parser = node_parser
    Settings.llm = llm

    index_name = "llamaindex-helper-documentation"
    pc_index = pc.Index(name=index_name)
    vector_store = PineconeVectorStore(pinecone_index=pc_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents=documents, storage_context=storage_context, show_progress=True
    )

    print("finish ingestion ....")
