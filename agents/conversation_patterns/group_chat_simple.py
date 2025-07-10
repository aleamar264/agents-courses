from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager

load_dotenv()

llm_config = {
    "model": "mistral:7b",
    # "model": "qwen3:8b",
    # "model": "gemma3:4b",
    # "model": "llama3.2",
    # "model": "deepseek-r1:8b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}

flight_agent = ConversableAgent(
    name="flight_agent",
    system_message="You provide the best flight options for the given destinations and dates",
    llm_config=llm_config,
    description="Provides flight options",
)

hotel_agent = ConversableAgent(
    name="hotel_agent",
    system_message="You recommend activities and attractions to visit at the destination",
    llm_config=llm_config,
    description="Recommend activities and attractions",
)

activity_agent = ConversableAgent(
    name="activity_agent",
    system_message="You recomment activities and attractions to visit at the destinations",
    llm_config=llm_config,
    description="Recommends activities and attractions",
)

restaurant_agent = ConversableAgent(
    name="restaurant_agent",
    system_message="You suggest the best restaurant to dine at in the destinations",
    llm_config=llm_config,
    description="Recommend restaurant",
)

weather_agent = ConversableAgent(
    name="weather_agent",
    system_message="You provide the weather forecast for the travel dates.",
    llm_config=llm_config,
    description="Provides weather forecast",
)

group_chat = GroupChat(
    agents=[flight_agent, hotel_agent, activity_agent, restaurant_agent, weather_agent],
    messages=[],
    max_round=6,
)

group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
chat_result = weather_agent.initiate_chat(
    group_chat_manager,
    message="I'm planning a trip to Paris for the first week of September. Can you help me plan? I will be departuring from Miami",
    summary_method="reflection_with_llm",
)
