from fastapi import Depends, Response, status, HTTPException, APIRouter
from app.database import get_db
from app.models.todid import Todid
from app.schemas.todid import TodidSchemaCreate, TodidSchemaResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todids", tags=["ToDid Endpoints"])

def find_todid(id: int, db: Session) -> Todid:
    return db.query(Todid).get(id)


@router.get(
        "/",
        response_model=list[TodidSchemaResponse],
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_todids(db: Session = Depends(get_db)) -> list[TodidSchemaResponse]:
    todids = db.query(Todid).all()
    return todids


@router.get(
        "/{id}",
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


@router.post(
        "/",
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


@router.put(
        "/{id}",
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


@router.delete(
        "/{id}",
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
