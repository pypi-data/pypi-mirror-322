import os
from typing import Optional, Any, Union

from pydantic import BaseModel


class Task(BaseModel):
    task: Union[str, tuple]
    model: Optional[str] = None
    key: Optional[str] = None
    base_url: Optional[str] = None

    def model_post_init(self, __context: Any) -> None:
        if isinstance(self.task, tuple):
            self.task = ' '.join(self.task)
