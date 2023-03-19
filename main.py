from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Todo(BaseModel):
    name: str
    completed: bool


todos = [
    Todo(
        name="Khoa",
        completed=True
    ),
    Todo(
        name="Khoa 1",
        completed=False
    ),
    Todo(
        name="Khoa 2",
        completed=False
    ),
    Todo(
        name="Khoa 3",
        completed=False
    )
]


@app.get("/")
def root():
    return {
        "title": "My Todo Khoa Tran Long Hao app",
        "todos": todos
    }
