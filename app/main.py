from fastapi import Depends, FastAPI, Response, status, HTTPException
from app import database
from app.models.todo import Todo
from app.schemas.todo import TodoSchemaCreate, TodoSchemaResponse
from .database import engine, get_db
from sqlalchemy.orm import Session

# Create any tables that don't exist
database.Base.metadata.create_all(bind=engine)

app = FastAPI()


def find_todo(id: int, db: Session) -> Todo:
    return db.query(Todo).get(id)


# path operation
# async is optional here
@app.get(
        "/",
        response_model=list[TodoSchemaResponse],
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_todos(db: Session = Depends(get_db)) -> list[TodoSchemaResponse]:
    todos = db.query(Todo).all()
    return todos


@app.get(
        "/todos/{id}",
        response_model=TodoSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_todo(id: int, db: Session = Depends(get_db)) -> TodoSchemaResponse:
    todo = find_todo(id, db)
    if not todo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )
    return todo


@app.post(
        "/todos",
        status_code=status.HTTP_201_CREATED,
        response_model=TodoSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def post_todo(todo: TodoSchemaCreate, db: Session = Depends(get_db)) -> TodoSchemaResponse:
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.put(
        "/todos/{id}",
        status_code=status.HTTP_202_ACCEPTED,
        response_model=TodoSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def put_todo(id: int, todo: TodoSchemaCreate, db: Session = Depends(get_db)) -> TodoSchemaResponse:
    update_query = db.query(Todo).filter(id == id)
    todo = update_query.first()
    if not todo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    update_query.update(todo.dict())
    db.commit()

    return update_query.first()


@app.delete(
        "/todos/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_model=None)
async def delete_todo(id: int, db: Session = Depends(get_db)) -> None:
    todo = find_todo(id, db)
    if not todo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    todo.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
