from autogen import  UserProxyAgent, ConversableAgent, AssistantAgent
import pandas as pd

llm_config = {
    # "model": "mistral:7b",
    # "model": "qwen3:8b",
    "model": "gemma3:4b",
    # "model": "llama3.2",
    # "model": "deepseek-r1:8b",
    "api_type": "ollama",
    "temperature": 0.3,
    # "client_host": "http://localhost:11434"
}

data_aggregation_agent = AssistantAgent(
    name="data_aggregation_agent",
    llm_config=llm_config,
    system_message="""
    You collected and aggregate financial data from the provided CSV file for the monthly financial report.
"""
)

report_generation_agent = AssistantAgent(
    name="report_generation_agent",
    llm_config=llm_config,
    system_message="""
    You generate detailed financial reports based on the aggregated data
"""
)

accuracy_review_agent = AssistantAgent(
    name="accuracy_review_agent",
    llm_config=llm_config,
    system_message="""
    You check the financial report for accuracy and consistency.
"""
)

compliance_review_agent = AssistantAgent(
    name="compliance_review_agent",
    llm_config=llm_config,
    system_message="""
    You ensure the financial report complies with financial regulations and standards.
    """
)

summary_generation_agent = AssistantAgent(
    name="summary_generation_agent",
    llm_config=llm_config,
    system_message="""
    You summarize the financial report for executive presentations.
    """
)

feedback_agent = AssistantAgent(
    name="feedback_agent",
    llm_config=llm_config,
    system_message="""
    You collect feedback from executives on the summary of the financial report
    """
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content","").find("TERMINATE")>=0,
    code_execution_config={
        "last_n_message": 1,
        "work_dir": "./agents/use_cases",
        "use_docker": False
    }
)

def read_csv_file():
    print("Reading CSV file...")
    df = pd.read_csv("./agents/use_cases/financial_data.csv")
    return df.to_dict()

user_proxy.register_nested_chats(
    [
        {
            "recipient": report_generation_agent,
            "message": lambda recipient, messages, sender, config: f"Generate a detailed financial report based on the following data: {read_csv_file()}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": accuracy_review_agent,
            "message": lambda recipient, messages, sender, config: f"Check this report for accuracy and consistency: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": compliance_review_agent,
            "message": lambda recipient, messages, sender, config: f"Ensure this report complies with financial regulations and standards: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": summary_generation_agent,
            "message": lambda recipient, messages, sender, config: f"Summarize the financial report for an executive presentation: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": feedback_agent,
            "message": lambda recipient, messages, sender, config: f"Collect feedback on this summary from executives: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
    ],
    trigger=data_aggregation_agent,
)

# Define the initial data aggregation task
initial_task = (
    """Collect and aggregate financial data for the monthly financial report."""
)

# Start the nested chat
user_proxy.initiate_chat(
    recipient=data_aggregation_agent,
    message=initial_task,
    max_turns=2,
    summary_method="last_msg",
)