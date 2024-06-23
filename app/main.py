from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Define the Todo model with pydantic
class TodoModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: Optional[int] = None
    label: Optional[str] = None
    parent: Optional[object] = None
    # remind: Optional[datetime] = None
    # due: Optional[datetime] = None

my_todos = [
    { "id": 1, "title":"todo 1" },
    { "id": 2, "title":"todo 2" }
]

def find_todo(id: int):
    for i, t in enumerate(my_todos):
        if t['id'] == id:
            return i, t
    return -1, None


# path operation
# async is optional here
@app.get("/")
async def get_todos():
    return { "data": my_todos }


@app.get("/todos/{id}")
async def get_todo(id: int):
    (index, todo) = find_todo(id)
    if index == -1:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    return { "data": todo }


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def post_todo(todo: TodoModel):
    todo_dict = todo.model_dump()
    todo_dict['id'] = randrange(0, 1000000000)
    my_todos.append(todo_dict)
    return { "data": todo_dict }


@app.put("/todos/{id}", status_code=status.HTTP_202_ACCEPTED)
async def put_todo(id: int, todo: TodoModel):
    (index, orig_todo) = find_todo(id)
    if index == -1:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    todo_dict = todo.model_dump()
    todo_dict['id'] = id
    my_todos[index] = todo_dict
    return { "data": todo_dict }


@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int):
    (index, todo) = find_todo(id)
    if index == -1:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    my_todos.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)