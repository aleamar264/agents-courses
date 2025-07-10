from autogen import AssistantAgent, UserProxyAgent

llm_config = [
    {
        "model": "gemma3:4b",
        "api_type": "ollama",
        # "client_host": "http://localhost:11434"
    },
    {
        "model": "llama3.2",
        "api_type": "ollama",
        # "client_host": "http://localhost:11434"
    },
    {
        "model": "deepseek-r1:7b",
        "api_type": "ollama",
        # "client_host": "http://localhost:11434"
    },
    {
        "model": "granite3.3:8b",
        "api_type": "ollama",
        # "client_host": "http://localhost:11434"
    }
]

llm = {
        "model": "gemma3:4b",
        "api_type": "ollama",
        # "client_host": "http://localhost:11434"
    }

assistant = AssistantAgent(name="assistant", llm_config=llm)
user_proxy = UserProxyAgent(
    name="user_proxy",
    llm_config=llm,
    code_execution_config=False,
    human_input_mode="NEVER"
)


# start the agents

user_proxy.initiate_chat(recipient=assistant, message="What is the capital of France?")
