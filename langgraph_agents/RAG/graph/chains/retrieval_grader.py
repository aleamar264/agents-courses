from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama.chat_models import ChatOllama
from graph.const import MODEL_OLLAMA

llm = ChatOllama(model=MODEL_OLLAMA)


class GradeDocuments(BaseModel):
    """Binay score for relevance check on retrieved documents"""

    binary_score: str = Field(
        description="The document is relevant to the question, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """
    You are a grader assesing relevance of a retrieval document to a user question.\n
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binaray score 'yes' or 'no' score to indicate whether the document is relevant to the question.
"""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {documents} \n\n User question {question}")
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader

