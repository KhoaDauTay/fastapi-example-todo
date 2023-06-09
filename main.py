from fastapi import FastAPI, Depends
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from schemas import TodoCreate, TodoUpdate

# DATABASE
SQLALCHEMY_DATABASE_URL = "sqlite:///app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is class of Session in DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # -> Type class


# -> 1 tap hop cac step de connect den db va mo ra session

def inject_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()


class TodoModel(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    completed = Column(Boolean)
    day_completed = Column(DateTime)
    user = Column(String(length=20))
    user_name = Column(String(length=20))


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
    return templates.TemplateResponse("index.html", {"request": request, "title": "Todo in thu 3"})


@app.get("/todos")
def get_todos(session=Depends(inject_session)):
    result = session.query(TodoModel).all()
    return {
        "todos": result
    }


@app.get("/todos/{name}")
def get_todo(name: str, session=Depends(inject_session)):
    result = session.query(TodoModel).filter_by(name=name).first()
    return {
        "todo": result
    }


@app.post("/todos")
def create_todo(data: TodoCreate, session=Depends(inject_session)):
    new_todo = TodoModel(
        name=data.name,
        completed=False
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo


@app.put("/todos/{name}")
def update_status_todo(
        name: str,
        data: TodoUpdate,
        session=Depends(inject_session)
):
    result = session.query(TodoModel).filter_by(name=name).first()
    if result:
        result.completed = data.completed
        session.commit()
        session.refresh(result)
        return {
            "todo": result
        }
    else:
        return {
            "message": f"Not found todo with name {name}"
        }


@app.delete("/todos/{name}")
def delete_todo(
        name: str,
        session=Depends(inject_session)
):
    result = session.query(TodoModel).filter_by(name=name).first()  # -> object of TodoModel
    if result:
        session.delete(result)
        session.commit()
        return {
            "message": f"Deleted {name}"
        }
    else:
        return {
            "message": f"Not found todo with name {name}"
        }

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
