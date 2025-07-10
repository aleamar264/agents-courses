from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import revisor, first_responder
from tool_executer import execute_tools
load_dotenv()


MAX_ITERATIONS = 2
builder = MessageGraph()
builder.add_node("draft", first_responder)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor)
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")

def event_loop(state: list[BaseMessage])->str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    if count_tool_visits > MAX_ITERATIONS:
        return END
    return "execute_tools"

builder.add_conditional_edges("revise", event_loop, {END:END, "execute_tools":"execute_tools"})
builder.set_entry_point("draft")
graph = builder.compile()
# print(graph.get_graph().draw_mermaid())

if __name__ == "__main__":
    input = HumanMessage(content="Write about AI-Powered SOC / autonomous SOC problems domains, list startups that do that and raised capital")
    res = graph.invoke(input)
    print(res)