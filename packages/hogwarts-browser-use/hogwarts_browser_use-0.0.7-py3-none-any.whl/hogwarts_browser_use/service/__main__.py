import asyncio

import click

from hogwarts_browser_use.model.task import Task
from hogwarts_browser_use.service.core import HogwartsBrowserUse
from hogwarts_browser_use.service.llm_factory import LLMFactory


@click.command()
@click.argument('task', nargs=-1)
@click.option('--model', '-m', default='gpt-4o-mini', type=str, help='model')
@click.option('--key', '-k', help='key')
@click.option('--base-url', '-u', default=None, type=str, help='base url')
def main(**kwargs):
    """
    霍格沃兹测试开发学社学员定制版 Browser-Use

    霍格沃兹测试开发学社 https://testing-studio.com

    测吧（北京）科技有限公司 https://ceba.ceshiren.com

    hogwarts-browser-use -m gpt-4o-mini 打开ceshiren.com 进入搜索 点击高级搜索 搜索python

    hogwarts-browser-use -m mistral 打开ceshiren.com 进入搜索 点击高级搜索 搜索python

    hogwarts-browser-use -m qwen2.5  打开ceshiren.com 进入搜索 点击高级搜索 搜索python
    """
    task = Task.model_validate(kwargs)
    llm = LLMFactory().get_llm(task=task)
    print(llm)

    service = HogwartsBrowserUse(llm=llm)
    asyncio.run(service.main(task=task))
