import os

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI


class LangChainOpenAIExecutor:
    def __init__(self, openai_api_key: str, open_ai_model: str = "gpt-4o-mini") -> None:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.__llm = ChatOpenAI(model="gpt-4o-mini")

    def run(self, prompt: str) -> BaseMessage:
        return self.__llm.invoke(prompt)
