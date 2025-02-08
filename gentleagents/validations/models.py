from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Any, List

T = TypeVar('T')

class ToolResponse(BaseModel, Generic[T]):  
    result: T
    message: str = Field(..., description="Message describing the result of the tool execution")

class TaskAssignment(BaseModel):
    agent: str
    task: str

class TaskResponse(BaseModel):
    task: TaskAssignment | None = None

class NextTaskResponse(BaseModel):
    continue_: bool = Field(..., alias="continue")
    task: TaskAssignment | None = None