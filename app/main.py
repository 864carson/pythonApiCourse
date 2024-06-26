from fastapi import FastAPI, Response, status, HTTPException
from app.models.todo_model import TodoModel
import psycopg2
from psycopg2.extras import RealDictCursor
# import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='todos', user='postgres', password='car04soN!30$', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection successful')
        break
    except Exception as error:
        print('connecting to db failed')
        print("Error: ", error)
        # time.sleep(2)


def find_todo(id: int):
    cursor.execute("""SELECT * FROM public."Todos" WHERE id=%s """, (str(id)))
    return cursor.fetchone()


# path operation
# async is optional here
@app.get("/")
async def get_todos():
    cursor.execute("""SELECT * FROM public."Todos" """)
    todos = cursor.fetchall()
    return { "data": todos }


@app.get("/todos/{id}")
async def get_todo(id: int):
    todo = find_todo(id)
    if not todo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    return { "data": todo }


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def post_todo(todo: TodoModel):
    cursor.execute("""INSERT INTO public."Todos" (title, description) VALUES (%s, %s) RETURNING * """, (todo.title, todo.description))
    new_todo = cursor.fetchone()
    conn.commit()
    return { "data": new_todo }


@app.put("/todos/{id}", status_code=status.HTTP_202_ACCEPTED)
async def put_todo(id: int, todo: TodoModel):
    cursor.execute("""UPDATE public."Todos" SET title=%s, description=%s WHERE id=%s RETURNING * """, (todo.title, todo.description, str(id)))
    updated_todo = cursor.fetchone()
    conn.commit()
    if not updated_todo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    return { "data": updated_todo }


@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int):
    cursor.execute("""DELETE FROM public."Todos" WHERE id=%s RETURNING * """, (str(id)))
    deleted_todo = cursor.fetchone()
    conn.commit()
    if not deleted_todo:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' was not found." )

    return Response(status_code=status.HTTP_204_NO_CONTENT)