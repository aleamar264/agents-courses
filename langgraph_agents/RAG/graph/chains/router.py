from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama.chat_models import ChatOllama
from graph.const import MODEL_OLLAMA

llm = ChatOllama(model=MODEL_OLLAMA, temperature=0)

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource"""
    datasource:Literal["vectorstore", "websearch"] = Field(..., description="Give a user question choose to route it to web search or a vector store")

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You're an expert at routing a user question to a vectorstore or web search.
 The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
 Use the vector store for questions on these topics. For all else, use web-search"""

route_prompt = ChatPromptTemplate.from_messages(
    [("system", system),
     ("human", "{question}")]
)

question_router = route_prompt | structured_llm_router