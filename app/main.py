from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/hi")
async def root():
    return {"message": "Hello World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}",
         response_model=schemas.UserBase
         )
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    todos = []

    for todo in db_user.todos:
        todos.append(schemas.Todo(
            title=todo.title,
            created_at=todo.created_at
        ))
    return schemas.UserBase(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        todos=todos
    )


@app.get("/todos/{user_id}"
         # response_model=
         )
def get_todos(user_id: int, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, user_id=user_id)
    return todos


@app.get("/health_check")
def get_todos(db: Session = Depends(get_db)):
    return "HELLO WORLD"
