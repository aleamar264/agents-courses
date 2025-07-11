from dotenv import load_dotenv

from langgraph.graph import END, StateGraph
from graph.const import RETRIEVE, GENERATE, GRADE_DOCUMENTS, WEBSEARCH
from graph.nodes import generate, grade_documents, retrieve, web_search
from graph.state import GraphState
from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.router import question_router, RouteQuery

load_dotenv()


def decide_to_generate(state: GraphState) -> str:
    print("---ASSES GRADED DOCUMENTS---")

    if state["web_search"]:
        print("---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE")
        return WEBSEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE

# ------------------ SELF RAG -------------------------------------------
def grade_generation_grounded_in_documets_and_quesions(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    docs = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke({"documents": docs, "generation": generation})
    if score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION VS QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION NOT ADDRESSES QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE---")
        return "not supported"
# ------------------ SELF RAG -------------------------------------------

def route_question(state:GraphState)->str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source :RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE
    return ""
workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

# ----Normal entry point ----------
# workflow.set_entry_point(RETRIEVE)
# ----Normal entry point ----------
workflow.set_conditional_entry_point(route_question, {WEBSEARCH:WEBSEARCH, RETRIEVE:RETRIEVE}, )
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS, decide_to_generate, {WEBSEARCH: WEBSEARCH, GENERATE: GENERATE}
)
# ------------------ SELF RAG -------------------------------------------
workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documets_and_quesions,
    {"not supported": GENERATE, "useful": END, "not useful": WEBSEARCH},
)
# ------------------ SELF RAG -------------------------------------------

workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid()
