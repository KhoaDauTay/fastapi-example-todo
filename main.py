from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy import Column, String, Boolean, Integer

from schemas import Todo, TodoCreate

# DATABASE
SQLALCHEMY_DATABASE_URL = "sqlite:///app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is class of Session in DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TodoModel(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    completed = Column(Boolean)


#
# Base.metadata.create_all(engine)


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


@app.get("/")
def root(request: Request):
    # Do something
    return templates.TemplateResponse("index.html", {"request": request, "title": "Khoa App todo"})


@app.get("/todos")
def get_todos():
    session = SessionLocal()
    result = session.query(TodoModel).all()
    session.close()
    return {
        "todos": result
    }


@app.get("/todos/{name}")
def get_todo(name: str):
    session = SessionLocal()
    result = session.query(TodoModel).filter_by(name=name).first()
    session.close()
    return {
        "todo": result
    }


@app.post("/todos")
def create_todo(data: TodoCreate):
    session = SessionLocal()
    new_todo = TodoModel(
        name=data.name,
        completed=False
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    session.close()
    return new_todo


# @app.put("/todos/{name}")
# def update_status_todo(
#         name: str,
#         data: TodoUpdate
# ):
#     for todo in todos:
#         if todo.name == name:
#             todo.completed = data.completed
#             return todo
#
#     return {
#         "message": f"Not found todo with name {name}"
#     }


# @app.delete("/todos/{name}")
# def delete_todo(
#         name: str,
# ):
#     for todo in todos:
#         if todo.name == name:
#             todos.remove(todo)
#             return {
#                 "message": f"Delete successfully {name}"
#             }
#     return {
#         "message": f"Not found todo with name {name}"
#     }


# @app.get("/todos-sqlraw")
# def get_todos():
#     my_session = SessionLocal()
#     query = text(
#         "SELECT * FROM todo"
#     )
#     rows = my_session.execute(query)
#     todos = []
#     for row in rows:
#         data = row.tuple()
#         todos.append(Todo(
#             name=data[1],
#             completed=True if data[2] == 1 else False
#         ))
#     my_session.close()
#     return {
#         "title": "My Todo Khoa Tran Long Hao app",
#         "todos": todos
#     }
