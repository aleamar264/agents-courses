from typing import Any
from src.RAG.graph.chains.generation import generation_chain
from src.RAG.graph.state import GraphState

def generate(state: GraphState)->dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    generation = generation_chain.invoke({"context": documents, "question":question})
    return {"documents":documents, "question":question, "generation": generation}
