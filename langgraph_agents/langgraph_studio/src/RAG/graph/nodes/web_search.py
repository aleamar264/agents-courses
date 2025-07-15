from typing import Any
from langchain.schema import Document
from langchain_tavily import TavilySearch

from src.RAG.graph.state import GraphState
from dotenv import load_dotenv

load_dotenv()

web_search_tool = TavilySearch(max_results=3)


def web_search(state: GraphState) -> dict[str, Any]:
    print("---WEB SEARCH---")
    question = state["question"]
    documents = state.get("documents")

    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs["results"]])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}


if __name__ == "__main__":
    web_search(state={"question": "agent memory", "documents": None})
