from autogen import ConversableAgent
from dotenv import load_dotenv

load_dotenv()

llm_config = [{
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
}]

agent_with_animal = ConversableAgent(
    name="agent_with_animal",
    system_message="You are thinking of animal. You have the animal 'elephant' in you mind, an I always try to guess it"
    "If I guess incorrectly, give a hint. Never mention the animal that you are thinking directly",
    llm_config={"config_list": llm_config},
    is_termination_msg= lambda msg: "elephant" in msg["content"],
    code_execution_config=False,
    human_input_mode="NEVER",
)

human_proxy = ConversableAgent(
    name="human_proxy",
    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",
)

result = human_proxy.initiate_chat(recipient=agent_with_animal, message="Parrot")