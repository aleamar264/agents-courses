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

agent = ConversableAgent(
    name="chatbot",
    llm_config={"config_list": llm_config},
    code_execution_config=False,
    human_input_mode="NEVER",
)


response = agent.generate_reply(
    messages=[{"role": "system", "content": "Tell me a fun joke"}]
)

print(response)