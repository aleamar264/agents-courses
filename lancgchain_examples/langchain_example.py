import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(api_key=openai_key, model="get-4")

messages = [
    SystemMessage(content="Translate the following from English to Italian"),
    HumanMessage(content="hi"),
]


res = model.invoke(messages)

print(res.content)
