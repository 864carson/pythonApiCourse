from fastapi import Depends, FastAPI, Response, status, HTTPException
from app import database, utils
from app.models.todid import Todid
from app.models.user import User
from app.schemas.todid import TodidSchemaCreate, TodidSchemaResponse
from app.schemas.user import UserSchemaCreate, UserSchemaResponse
from .database import engine, get_db
from sqlalchemy.orm import Session


# Create any tables that don't exist
database.Base.metadata.create_all(bind=engine)

app = FastAPI()


def find_todid(id: int, db: Session) -> Todid:
    return db.query(Todid).get(id)


# path operation
# async is optional here
@app.get(
        "/",
        response_model=list[TodidSchemaResponse],
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_todids(db: Session = Depends(get_db)) -> list[TodidSchemaResponse]:
    todids = db.query(Todid).all()
    return todids


@app.get(
        "/todids/{id}",
        response_model=TodidSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_todid(id: int, db: Session = Depends(get_db)) -> TodidSchemaResponse:
    todid = find_todid(id, db)
    if not todid:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"ToDid with id '{id}' was not found." )
    return todid


@app.post(
        "/todids",
        status_code=status.HTTP_201_CREATED,
        response_model=TodidSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def post_todid(todid: TodidSchemaCreate, db: Session = Depends(get_db)) -> TodidSchemaResponse:
    new_todid = Todid(**todid.model_dump())
    db.add(new_todid)
    db.commit()
    db.refresh(new_todid)
    return new_todid


@app.put(
        "/todids/{id}",
        status_code=status.HTTP_202_ACCEPTED,
        response_model=TodidSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def put_todid(id: int, todid: TodidSchemaCreate, db: Session = Depends(get_db)) -> TodidSchemaResponse:
    update_query = db.query(Todid).filter(id == id)
    todid = update_query.first()
    if not todid:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"ToDid with id '{id}' was not found." )

    update_query.update(todid.dict())
    db.commit()

    return update_query.first()


@app.delete(
        "/todids/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_model=None)
async def delete_todid(id: int, db: Session = Depends(get_db)) -> None:
    todid = find_todid(id, db)
    if not todid:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"ToDid with id '{id}' was not found." )

    todid.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get(
        "/users",
        response_model=list[UserSchemaResponse],
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_users(db: Session = Depends(get_db)) -> list[UserSchemaResponse]:
    users = db.query(User).all()
    return users


@app.post(
        "/users",
        status_code=status.HTTP_201_CREATED,
        response_model=UserSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def post_user(user: UserSchemaCreate, db: Session = Depends(get_db)) -> UserSchemaResponse:
    # Hash the password
    user.password = utils.hash(user.password)

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
