import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from hogwarts_browser_use.model.task import Task


class LLMFactory:
    def get_llm(self, task: Task):
        if task.model.startswith('gpt'):
            llm = ChatOpenAI(
                model_name=task.model,
                temperature=0,
                openai_api_key=SecretStr(task.key or os.environ.get('OPENAI_API_KEY')),
                openai_api_base=task.base_url or os.environ.get('OPENAI_API_BASE') or os.environ.get('OPENAI_BASE_URL'),
            )
            return llm

        else:
            llm = ChatOllama(
                model=task.model,
                temperature=0,
                base_url=task.base_url or 'http://127.0.0.1:11434'
            )
            return llm
