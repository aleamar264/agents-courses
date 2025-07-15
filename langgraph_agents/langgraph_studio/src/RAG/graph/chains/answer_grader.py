from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama
from src.RAG.graph.const import MODEL_OLLAMA

llm = ChatOllama(model=MODEL_OLLAMA, temperature=0)

class GradeAnswer(BaseModel):
    binary_score: bool = Field(description="Answer addresses the question, 'yes' or 'no'")

structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """You are a grader assessing whether an asnswer is addresses / resolves the question\n
Give a binary score 'yes' or 'no' 'Yes' means that the answer resolves the question"""


answer_promt = ChatPromptTemplate(
    [("system", system),
     ("human", "User question:\n\n {question} \n\n LLM generation {generation}")]
)

answer_grader: RunnableSequence = answer_promt | structured_llm_grader