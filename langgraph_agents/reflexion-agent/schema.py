from pydantic import BaseModel, Field


class Reflection(BaseModel):
    """Reflection"""
    missing: str = Field(description="Critique of what is missing")
    superfluous: str = Field(description="Critique what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question"""

    answer: str = Field(description="~250 words detailed answer to the question")
    reflection: Reflection = Field(description="Your reflection on the initial answer")
    search_queries: list[str] = Field(
        description="1 - 3 queries for researching improvements to address the critique of your current answer"
    )


class RevisedAnswer(AnswerQuestion):
    """Revise your original answer to your question"""
    references: list[str] = Field(description="Citations motivating your updated answer")