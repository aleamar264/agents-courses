from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
import subprocess
from time import perf_counter
import sys

start = perf_counter()

# llm = Ollama("llama3.2")
# llm = Ollama("gemma2:2b")
# the fastest model in a single GPU and balanced
# https://ollama.com/library/gemma3
llm = Ollama("gemma3:4b")
# llm = Ollama("deepseek-r1:7b", request_timeout=300)

# llm = Ollama("granite3.3:8b", request_timeout=60)

def write_haiku(topic: str)->str:
    """Writes a haiku about a given topic"""
    return llm.complete(f"Write me a haiku about {topic}").text

def count_characteres(text:str)-> int:
    """Count the characteres in a text"""
    return len(text)

def open_application(application_name:str)->str:
    try:
        if sys.platform == "linux":
            subprocess.Popen([application_name.lower()])
        if sys.platform == "win32":
            subprocess.Popen()
        if sys.platform == "macos":
            subprocess.Popen(["/usr/bin/open", "-n", "-a", application_name.lower()])
        return "succesfully opened the application"
    except Exception as e:
        return f"Error: {str(e)}"

def open_url(url:str)->str:
    """Open an url in browser"""
    try:
        if sys.platform == "linux":
            subprocess.Popen(["xdg-open", url.lower()])
        if sys.platform == "win32":
            subprocess.Popen()
        if sys.platform == "macos":
            subprocess.Popen(["/usr/bin/open", "--url", url])
        return "succesfully opened the url"
    except Exception as e:
        return f"Error: {str(e)}"
if __name__ == "__main__":
    tool1 = FunctionTool.from_defaults(fn=write_haiku, name="write_haiku")
    tool2 = FunctionTool.from_defaults(fn=count_characteres, name="count_characteres")
    tool3 = FunctionTool.from_defaults(fn=open_application, name="open_application")
    tool4 = FunctionTool.from_defaults(fn=open_url, name="open_url")

    agent = ReActAgent.from_tools(tools=[tool1, tool2, tool3, tool4], llm=llm, verbose=True)

    # res = agent.query("Write me a haiku about tennis and count the characteres in it")
    # res = agent.query("Open dbeaver in my computer")
    res = agent.query("Write a haiku about beatiful woman and open url https://google.com")
    print(res)
    print(perf_counter() - start)