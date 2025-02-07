from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Any

T = TypeVar('T')

class ToolResponse(BaseModel, Generic[T]):  
    result: T
    message: str = Field(..., description="Message describing the result of the tool execution")
