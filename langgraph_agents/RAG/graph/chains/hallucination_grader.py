from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_ollama.chat_models import ChatOllama
from graph.const import MODEL_OLLAMA

llm = ChatOllama(model=MODEL_OLLAMA, temperature=0)


class GradeHallucination(BaseModel):
    """Binay score for hallucination present in generation answer"""

    binary_score: bool = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeHallucination)

system = """You're a grader assesing whether an LLM generation is grounded in / supported by a set of  retrieved facts.
Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by set of facts"""


hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation {generation}"),
    ]
)


hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader