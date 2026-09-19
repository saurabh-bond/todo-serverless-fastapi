import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from src.config import settings


class TodoService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(settings.TABLE_NAME)

    def get_all_todos(self):
        try:
            response = self.table.scan()
            return response.get("Items", [])
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {e.response['Error']['Message']}"
            )

    def create_todo(self, todo_id: str, title: str, description: str):
        try:
            item = {
                "todo_id": todo_id,
                "title": title,
                "description": description,
                "completed": False
            }
            self.table.put_item(item=item)
            return item
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create item: {e.response['Error']['Message']}"
            )