from pydantic import BaseModel


class Todo(BaseModel):
    name: str
    completed: bool


class TodoCreate(BaseModel):
    name: str


class TodoUpdate(BaseModel):
    completed: bool
