from dotenv import load_dotenv
from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from ingestion import retriever
from pprint import pprint
from generation import generation_chain
from graph.chains.hallucination_grader import hallucination_grader, GradeHallucination
from graph.chains.router import question_router, RouteQuery

load_dotenv()

def test_retrival_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_txt = docs[1].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "yes"


def test_teneration_chain()-> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs, "question":question})
    pprint(generation)


def test_hallucination_grader_answer_yes()->None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs, "question": question})
    res: GradeHallucination = hallucination_grader.invoke({"documents": docs, "generation": generation})
    assert res.binary_score


def test_router_vectorstore()->None:
    question = "agent memory"
    res: RouteQuery = question_router.invoke({"question":question})
    assert res.datasource == "vectorstore"


def test_router_websearch()->None:
    question = "how to make pizza"
    res: RouteQuery = question_router.invoke({"question":question})
    assert res.datasource == "websearch"