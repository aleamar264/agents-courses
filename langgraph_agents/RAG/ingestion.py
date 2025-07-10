from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings

load_dotenv()

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm",
]

docs = [WebBaseLoader(url).load() for url in urls]
doc_list = [item for sublist in docs for item in sublist]
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

docs_splits = text_splitter.split_documents(doc_list)

# vectorstore = Chroma.from_documents(
#     documents=docs_splits,
#     collection_name="rag-chroma",
#     embedding=OllamaEmbeddings(model="mxbai-embed-large:335m"),
#     persist_directory="./langgraph_agents/RAG",
# )

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./langgraph_agents/RAG",
    embedding_function=OllamaEmbeddings(model="mxbai-embed-large:335m"),
).as_retriever()

