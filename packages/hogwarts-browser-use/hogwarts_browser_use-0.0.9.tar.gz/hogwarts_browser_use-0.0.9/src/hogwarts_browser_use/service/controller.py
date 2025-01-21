import asyncio

from browser_use.agent.views import ActionResult
from browser_use.controller.service import Controller as BaseController, logger
from pydantic import BaseModel, Field


class SleepParam(BaseModel):
    timeout: float = Field(default=2, description='等待时长，以秒为单位')


class Controller(BaseController):

    def __init__(self):
        super().__init__()
        self.init_actions()

    def init_actions(self):
        @self.registry.action(
            'wait sleep',
            param_model=SleepParam,
            requires_browser=True,
        )
        async def sleep(param: SleepParam):
            msg = f'sleep {param.timeout}'
            await asyncio.sleep(param.timeout)
            logger.info(msg)
            return ActionResult(extracted_content=msg, include_in_memory=True)
