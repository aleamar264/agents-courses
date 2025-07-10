from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager

load_dotenv()

llm_config = {
    # "model": "mistral:7b",
    # "model": "qwen3:8b",
    "model": "gemma3:4b",
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
    system_message="You suggest the best hotels for the given destination and dates.",
    llm_config=llm_config,
    description="Suggests hotel options.",
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

group_chat_with_introductions = GroupChat(
    agents=[flight_agent, hotel_agent, activity_agent, restaurant_agent, weather_agent],
    messages=[],
    max_round=6,
    send_introductions=True,
)

group_chat_manager_with_intro = GroupChatManager(
    groupchat=group_chat_with_introductions, llm_config=llm_config
)

travel_planner_agent = ConversableAgent(
    name="traveler_planner_agent",
    system_message="You summarize the travel plan provided by the group chat",
    llm_config=llm_config,
    description="Summarize the travel plan"
)

chat_result = travel_planner_agent.initiate_chats(
    [{
        "recipient": group_chat_manager_with_intro,
        "message": "I'm planning a trip to Paris for the first week of September. Can you help me plan? I will be leaving from Miami and will stay for a week",
        "summary_method": "reflection_with_llm"
    },
    {
        "recipient": group_chat_manager_with_intro,
        "message": "Please refine the plan with additional details",
        "summary_method": "reflection_with_llm"
    }]
)

# for result in chat_result:
#     print(result.cost)
#     print(result.summary)
