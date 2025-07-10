from datetime import datetime
from dotenv import load_dotenv
from langchain_core.output_parsers import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from schema import AnswerQuestion, RevisedAnswer

llm = ChatOllama(model="qwen3:8b", temperature=0.5)
parser = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])

load_dotenv()

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You're expert researcher.
            Current time: {time}
            1. {first_instruction}
            2. Provide a reflection with the following fields:
               - missing: What is lacking in your answer
               - superfluous: What is unnecessary in your answer
            3. Recommend search queries to research information and improve your answer""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
).partial(time=lambda: datetime.now().isoformat())


first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)


first_responder = (
    first_responder_prompt_template
    | llm.bind_tools(tools=[AnswerQuestion], tool_choice={"type": "AnswerQuestion"})

)

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the world limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove the superfluous information from your answer and make SURE it is not more that 250 words"""


revisor = (
    actor_prompt_template.partial(first_instruction=revise_instructions)
    | llm.bind_tools(tools=[RevisedAnswer], tool_choice={"type": "RevisedAnswer"})
)

if __name__ == "__main__":
    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous SOC problems domains,"
        " list startups that do that and raised capital"
    )

    chain = first_responder | parser_pydantic

    res = first_responder.invoke(input={"messages": [human_message]})
    print(res)
