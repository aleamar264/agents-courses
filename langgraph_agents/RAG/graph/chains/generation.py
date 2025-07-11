from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
from graph.const import MODEL_OLLAMA

llm = ChatOllama(model=MODEL_OLLAMA, temperature=0)
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()

