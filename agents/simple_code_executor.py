from autogen import AssistantAgent, UserProxyAgent


llm_user = {
    "model": "gemma3:4b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}

llm_coder = {
    "model": "qwen2.5-coder:7b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}

assistant = AssistantAgent(name="assistant", llm_config=llm_coder)
user_proxy = UserProxyAgent(
    name="user_proxy",
    llm_config=llm_user,
    human_input_mode="ALWAYS",
    code_execution_config={"work_dir": "./agents/coding", "use_docker": False},
)


user_proxy.initiate_chat(recipient=assistant, message="Plot a chart of META and TESLA stock price, I using wsl2")