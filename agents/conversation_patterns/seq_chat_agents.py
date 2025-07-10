from dotenv import load_dotenv
from autogen import ConversableAgent

load_dotenv()

llm_config = {
    # "model": "mistral:7b",
    # "model": "qwen3:8b",
    "model": "gemma3:4b",
    # "model": "deepseek-r1:8b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}

initial_agent = ConversableAgent(
    name="initial_agent",
    system_message="You return me the text I give you",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

uppercase_agent = ConversableAgent(
    name="uppercase_agent",
    system_message="You convert the text I give you to uppercase",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

wordcount_agent = ConversableAgent(
    name="word_count_agent",
    system_message="You count the numbers of words in the text I give you",
    llm_config=llm_config,
    human_input_mode="NEVER",
)
reverse_agent = ConversableAgent(
    name="reverseText_agent",
    system_message="You reverse the text I give you",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

summarize_agent = ConversableAgent(
    name="sumarize_agent",
    system_message="You summarize the text I give you",
    llm_config=llm_config,
    human_input_mode="NEVER",
)


chat_result = initial_agent.initiate_chats(
    [
        {
            "recipient": uppercase_agent,
            "message": "This is a sample text document.",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": wordcount_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": reverse_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
                {
            "recipient": summarize_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
    ]
)

print(f"First chat summarize {chat_result[0].summary}")
print(f"Second chat summarize {chat_result[1].summary}")
print(f"Third chat summarize {chat_result[2].summary}")
print(f"Forth chat summarize {chat_result[3].summary}")
