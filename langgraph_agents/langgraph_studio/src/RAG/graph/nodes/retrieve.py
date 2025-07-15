from typing import Any
from src.RAG.graph.state import GraphState
from src.RAG.ingestion import retriever


def retrieve(state:GraphState)->dict[str, Any]:
    print("---Retrieve---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question":question}
