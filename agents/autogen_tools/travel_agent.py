from typing import Annotated
from dotenv import load_dotenv
from autogen import ConversableAgent

load_dotenv()

llm_config = {
    # "model": "mistral:7b",
    "model": "qwen3:8b",
    "api_type": "ollama",
    # "client_host": "http://localhost:11434"
}


def get_flight_status(flight_number: Annotated[str, "Flight number"]) -> str:
    print(flight_number)
    dummy_data = {"AA123": "On time", "DL456": "Delayed", "UA789": "Cancelled"}
    return f"The current status of the flight {flight_number} is {dummy_data.get(flight_number, 'unknown')}"


def get_hotel_info(location: Annotated[str, "Location"]) -> str:
    dummy_data = {
        "New York": "Top hotel in New York: The Plaza - 5 stars",
        "Los Angeles": "Top hotel in Los Angeles: The Beverly Hill - 5 stars",
        "Chicago": "Top hotel in Chicago: The Langhan - 5 stars",
    }
    return dummy_data.get(location, f"No hotels found in {location}")


def get_travel_advice(location: Annotated[str, "Location"]) -> str:
    dummy_data = {
        "New York": "Travel advice for New York: Visit Central Park and Times Square.",
        "Los Angeles": "Travel advice for Los Angeles: Check out Hollywood and Santa Monica Pier.",
        "Chicago": "Travel advice for Chicago: Don't miss the Art Institute and Millennium Park.",
    }
    return dummy_data.get(location, f"No travel advice available for {location}")


assistant = ConversableAgent(
    name="TravelerAssistant",
    system_message="You are a helpful AI traveler assistant. Return 'TERMINATE' when the task is done.",
    llm_config=llm_config,
)

user_proxy = ConversableAgent(
    name="User",
    is_termination_msg=lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register tools
assistant.register_for_llm(
    name="get_flight_status",
    description="Get the current status of a flight based on the flight number",
)(get_flight_status)

assistant.register_for_llm(
    name="get_hotel_info",
    description="Get information about the hotels in a specific location",
)(get_hotel_info)
assistant.register_for_llm(
    name="get_travel_advice", description="Get travel advice from a specific location"
)(get_travel_advice)


# Register action for the user proxy
user_proxy.register_for_execution("get_flight_status")(get_flight_status)
user_proxy.register_for_execution("get_hotel_info")(get_hotel_info)
user_proxy.register_for_execution("get_travel_advice")(get_travel_advice)


user_proxy.initiate_chat(
    assistant,
    message="What is the current status of the flight AA123? After that I'm traveling to New York , could you tell me about the hotel and what to do",
)
