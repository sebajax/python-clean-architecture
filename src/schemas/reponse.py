from pydantic import BaseModel
from typing import Any, Dict

class Response(BaseModel):
    error: bool = False
    data: Dict = {}

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)