An agent decide the flow of execution.
The agents can be no reliable:
- Task ambiguity
- LLM non-determinism
- Tool misuse
- Hallucinations
- ... and more

In the other hand, the chain is not flexible but more reliable

**LangGraph** is a solution that is flexible and reliable using ***State Machine***.

## Graph
This came from [Graph theory - Wikipedia](https://en.wikipedia.org/wiki/Graph_theory)


## State Machine
>The state machine pattern is a behavioral design pattern that allows an object to alter its behavior based on its internal state. It's a way to model systems that can be in a finite number of distinct states, with transitions between these states triggered by events or conditions. This pattern promotes cleaner, more maintainable code by encapsulating state-specific logic into separate state objects, rather than relying on numerous conditional statements within a single class. Google

## Flow Engineering
1. We want to define the FLOW (the scope), we don't want the LLM to start and do whatever it want.

## LangGraph Elements
- Nodes: Are python Functions
	- Start Node: First functions to do.
	- End Node: Last functions to do.
- Edges
- Conditional Edges
- Cyclic Graph
- Human in the loop
- Persistence


We are using LangSmith to have the tracing of how is the way that act the agents, we can traces the agents created with LangChain (seamless integration) or any other one. For more information of how to ingreate LangSmith with LangChain/Other framework please refer to [Add observability to your LLM application | 🦜️🛠️ LangSmith](https://docs.smith.langchain.com/observability/tutorials/observability)

## Examples
### Reflect Agents
**main.py**
```python
from dotenv import load_dotenv
from typing import Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generate_chain, reflect_chain


load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"

def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})

def reflection_node(messages: Sequence[BaseMessage])->list[BaseMessage]:
    res = reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res)]


builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

def should_continue(state: list[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)
graph = builder.compile()
print(graph.get_graph().draw_mermaid())

if __name__ == "__main__":
    print("Hello LangGraph")
    inputs = HumanMessage(content="""Make this tweet better:"
                          @LangChainAI

            - newly tool Calling feature is seriously underrated.

            After a long wait, it's here- making the implementation of agents across different model with function calling - super easy.

            Made a video covering their newest blog post.
""")
    response = graph.invoke(inputs)
```
**chains.py**
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama.llms import OllamaLLM

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate a critique and recommendations for the user"
            "Always provide detailed recommendations, including request for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request"
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ],
)

llm = OllamaLLM(model="mistral:7b")
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm
```
### Reflexion Agents
**main.py**
Here we have a little difference with the video, he use OpenAI, here we use Ollama for free models, in this case we are using Qwen3. The most important thing is the prompt. The original prompt was:
- You're expert researcher.
	Current time: {time}
	1. {first_instruction}
	2. Reflect and critique your answer. Be severe to maximize improvement.
	3. Recommend search queries to research information and improve your answer

After a good time making debugging and asking in internet I found that I need to explicitly tell to the model how I want the response, with this we get the following prompt:
- You're expert researcher.
	Current time: {time}
		1. {first_instruction}
		2. Provide a reflection with the following fields:
		   - missing: What is lacking in your answer
		   - superfluous: What is unnecessary in your answer
		3. Recommend search queries to research information and improve your answer
```python
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.output_parsers import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from schemas import AnswerQuestion

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


llm_with_tools = llm.bind_tools(
    tools=[AnswerQuestion],
    tool_choice={"type": "AnswerQuestion"}
)

chain = first_responder_prompt_template | llm_with_tools | parser_pydantic

if __name__ == "__main__":
    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous SOC problems domains,"
        " list startups that do that and raised capital"
    )

    res = chain.invoke(input={"messages": [human_message]})
    print(res)

```
**schemas.py**
```python
from pydantic import BaseModel, Field


class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing")
    superfluous: str = Field(description="Critique what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question"""

    answer: str = Field(description="~250 words detailed answer to the question")
    reflection: Reflection = Field(description="Your reflection on the initial answer")
    search_queries: list[str] = Field(
        description="1 - 3 queries for researching improvements to address the critique of your current answer"
    )

```
### Agentic RAG
### ReAct
### Persistence
