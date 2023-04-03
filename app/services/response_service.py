"""
global response service for all the use cases
"""

from pydantic import BaseModel


class ResponseService(BaseModel):
    """class to represent the services exception to return to  presentation layer"""
    detail: str
    data: dict | None = None
