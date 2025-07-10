from dotenv import load_dotenv
from autogen import ConversableAgent

load_dotenv()

traveler_config = {
    # "model": "mistral:7b",
    # "model": "qwen3:8b",
    "model": "gemma3:4b",
    # "model": "deepseek-r1:8b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}
guide_config = {
    # "model": "mistral:7b",
    # "model": "qwen3:8b",
    "model": "gemma3:4b",
    # "model": "deepseek-r1:8b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}



traveler_agent = ConversableAgent(
    name="Traveler_Agent",
    system_message="You are a traveler planning vacation",
    llm_config=traveler_config,
)

guide_agent = ConversableAgent(
    name="Guide_Agent",
    system_message="You are a travel guide with extensive knowledge about popular destinations",
    llm_config=guide_config,
)

chat_result = traveler_agent.initiate_chat(recipient=guide_agent,
                                           message="Waht are the must-see attractions in Tokyo?",
                                           summary_method="reflection_with_llm",
                                           max_turns=2)

# print(chat_result)
print("\n ***Chat summary***")
print(chat_result.summary)