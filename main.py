from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

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
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Todo(BaseModel):
    name: str
    completed: bool


todos = [
    Todo(
        name="Khoa",
        completed=True
    ),
    Todo(
        name="Khoa1",
        completed=False
    ),
    Todo(
        name="Khoa2",
        completed=False
    ),
    Todo(
        name="Khoa3",
        completed=False
    )
]


@app.get("/")
def root(request: Request):
    # Do something
    return templates.TemplateResponse("index.html", {"request": request, "title": "Khoa App todo"})


@app.get("/todos")
def get_todos():
    # Do something
    return {
        "title": "My Todo Khoa Tran Long Hao app",
        "todos": todos
    }


# Schema
class TodoCreate(BaseModel):
    name: str


class TodoUpdate(BaseModel):
    completed: bool


@app.post("/todos")
def create_todo(data: TodoCreate):
    new_todo = Todo(
        name=data.name,
        completed=False
    )
    todos.append(new_todo)
    return new_todo


@app.put("/todos/{name}")
def update_status_todo(
        name: str,
        data: TodoUpdate
):
    for todo in todos:
        if todo.name == name:
            todo.completed = data.completed
            return todo

    return {
        "message": f"Not found todo with name {name}"
    }


@app.delete("/todos/{name}")
def delete_todo(
        name: str,
):
    for todo in todos:
        if todo.name == name:
            todos.remove(todo)
            return {
                "message": f"Delete successfully {name}"
            }
    return {
        "message": f"Not found todo with name {name}"
    }
