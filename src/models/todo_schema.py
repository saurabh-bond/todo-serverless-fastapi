from typing import Optional
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class TodoResponse(BaseModel):
    todo_id: str
    title: str
    description: str
    completed: bool