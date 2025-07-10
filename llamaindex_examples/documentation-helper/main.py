from dotenv import load_dotenv
import os
from pinecone import Pinecone
from llama_index.core import (
    VectorStoreIndex,
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.settings import Settings
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager

from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.chat_engine.context import ContextChatEngine
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.prompts import PromptTemplate
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.response_synthesizers.type import ResponseMode
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from duplicate_postprocess import DuplicateRemoverNodePostProcessor
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import streamlit as st

llm = Ollama("llama3.2", temperature=0.0, request_timeout=200)
# embed_model = OllamaEmbedding(
#     model_name="nomic-embed-text:latest", embed_batch_size=100
# )
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5", embed_batch_size=100, device="cuda"
)
Settings.llm = llm
Settings.embed_model = embed_model


@st.cache_resource(show_spinner=False)
def get_index() -> VectorStoreIndex:
    load_dotenv()
    pc = Pinecone(api_key=os.getenv("PINECONE_API"))

    print("RAG...")
    pc_index = pc.Index("llamaindex-helper-documentation")
    vector_store = PineconeVectorStore(pc_index)

    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    Settings.callback_manager = CallbackManager(handlers=[llama_debug])

    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


index = get_index()
if "chat_engine" not in st.session_state.keys():
    fallback_prompt = PromptTemplate(
        "You are a helpful assistant. Here is some context:\n{context_str}\n\n"
        "Question: {query_str}\n\n"
        "Answer the question directly. If the context does not contain the answer, IGNORE IT and use your own knowledge."
    )
    response_synthesizer = get_response_synthesizer(
        llm=Settings.llm,
        text_qa_template=fallback_prompt,
        response_mode=ResponseMode.COMPACT,
        # streaming=True
    )
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=20,  # Reduce to only top 2 results
        filter_threshold=0.7,  # Increase threshold to exclude low-confidence matches
    )
    st.session_state.chat_engine = ContextChatEngine.from_defaults(
        retriever=retriever,
        llm=Settings.llm,
        verbose=True,
        use_async=True,
        response_synthesizer=response_synthesizer,
    )
    # postprocessor = SentenceEmbeddingOptimizer(
    #     embed_model=Settings.embed_model, percentile_cutoff=0.5, threshold_cutoff=0.7
    # )
    # query_engine = index.as_query_engine(llm=Settings.llm)
    # st.session_state.chat_engine = index.as_chat_engine(
    #     chat_mode=ChatMode.CONTEXT,
    #     verbose=True,
    #     query_engine=query_engine,
    #     # text_qa_template=fallback_prompt,
    #     # response_mode=ResponseMode.COMPACT,
    #     llm=Settings.llm
    #     # node_postprocessors=[postprocessor, DuplicateRemoverNodePostProcessor()],
    # )

st.set_page_config(
    page_title="Chat with LlamaIndex docs, powered by LlamaIndex",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("Chat with LlamaIndex docs 💬🦙")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about LlamaIndex's open source python library!",
        }
    ]

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            if prompt is not None:
                response = st.session_state.chat_engine.chat(message=prompt)
                nodes = [node for node in response.source_nodes]
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
