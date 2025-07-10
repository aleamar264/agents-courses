from autogen import AssistantAgent, UserProxyAgent

llm_config = {
    # "model": "mistral:7b",
    # "model": "qwen3:8b",
    "model": "gemma3:4b",
    # "model": "llama3.2",
    # "model": "deepseek-r1:8b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}

# Define the writer agent

writer = AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""
    You are a professional writer, known for you insightful and engaging product reviews.
    You transform technical details into compelling narratives.
    You should improve the quality of the content based on the feedback from the user.
""",
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "./agents/conversation_patterns",
        "use_docker": False,
    },
)

# Define the critic agent
critic = AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""
    You are a critic, known for you thoroughness and commitments to standards.
    Your task is to scrutinize content for any harmful or regulatory violations, ensuring
    all the material aling with required guidelines.
    """,
)


def reflection_message(recipient, messages, sender, config):
    print("reflecting..")
    return f"Reflect and provide critique on the following review. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"


user_proxy.register_nested_chats(
    [{
        "recipient": critic,
        "message": reflection_message,
        "summary_method": "last_msg",
        "max_turns": 1
    }],
    trigger=writer
)

task = """Write a detailed and engaging product review for the new Meta VR headset"""
res = user_proxy.initiate_chat(
    recipient=writer, message=task, max_turns=2, summary_method="last_msg"
)