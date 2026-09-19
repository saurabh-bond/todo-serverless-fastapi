import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from src.models.todo_schema import TodoCreate, TodoResponse
from src.services.dynamodb_service import TodoService
from src.dependencies import get_current_user

router = APIRouter()

def get_todo_service():
    return TodoService()

@router.get("/", response_model=List[TodoResponse])
def list_todos(
    service: TodoService = Depends(get_todo_service),
    current_user: dict = Depends(get_current_user)
):
    return service.get_all_todos()

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def add_todo(
    payload: TodoCreate, 
    service: TodoService = Depends(get_todo_service),
    current_user: dict = Depends(get_current_user)
):
    todo_id = str(uuid.uuid4())
    return service.create_todo(
        todo_id=todo_id,
        title=payload.title,
        description=payload.description
    )