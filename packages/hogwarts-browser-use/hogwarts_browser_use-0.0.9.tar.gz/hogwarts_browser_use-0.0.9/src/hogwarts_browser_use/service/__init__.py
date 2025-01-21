import os

from hogwarts_browser_use.service.__main__ import agent as agent_fun
from hogwarts_browser_use.service.llm_factory import LLMFactory


def agent(task: str, model: str = None):
    agent_fun(task=task, model=model)


__all__ = [
    'agent',
]
