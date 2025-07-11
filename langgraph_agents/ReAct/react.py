from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_ollama.chat_models import ChatOllama
from langchain_tavily import TavilySearch

load_dotenv()



@tool
def triple(num: float)->float:
    """
    param num: a number to triple
    returns: the triple of the input number
    """
    return num * 3

tools = [TavilySearch(max_results=1), triple]

llm = ChatOllama(model="llama3.2:latest", temperature=0).bind_tools(tools=tools)

