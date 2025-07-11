from typing import Any
from graph.chains.retrieval_grader import retrieval_grader, GradeDocuments
from graph.state import GraphState


def grade_documents(state: GraphState) -> dict[str, Any]:
    """Determines whether the retrieved documents are relevant to the question
    If any document is not relevant , we will set a flag to run web search

    Args:
        state (dict): The current graph state
    Returns:
        state(dict[str, Any]): Filtered out irrelevant documents and update web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    filtered_docs = []
    web_search = False
    for d in documents:
        score:GradeDocuments  = retrieval_grader.invoke(
            {"question": question, "documents": d.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT ---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT ---")
            web_search = True
            continue
    return {"documents": filtered_docs, "question": question, "web_search": web_search}


