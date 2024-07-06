from typing import Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from app import oauth2
from app.database import get_db
from app.models.todid import Todid
from app.schemas.todid import TodidSchemaCreate, TodidSchemaResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todids", tags=["ToDid Endpoints"])


@router.get(
        "/",
        response_model=list[TodidSchemaResponse],
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_todids(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = ""
    ) -> list[TodidSchemaResponse]:
    todids = db.query(Todid).filter(Todid.title.contains(search)).offset(offset).limit(limit).all()
    return todids


@router.get(
        "/{id}",
        response_model=TodidSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_todid(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ) -> TodidSchemaResponse:
    todid = db.query(Todid).get(id)
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
async def post_todid(
        todid: TodidSchemaCreate,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ) -> TodidSchemaResponse:
    new_todid = Todid(createdBy=current_user.id, **todid.model_dump())
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
async def put_todid(
        id: int,
        todid: TodidSchemaCreate,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ) -> TodidSchemaResponse:
    update_query = db.query(Todid).filter(Todid.id == id)
    todid = update_query.first()
    if not todid:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"ToDid with id '{id}' was not found." )

    # Validate the user owns the todid item
    if todid.createdBy != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action")

    update_query.update(todid.dict(), synchronize_session=False)
    db.commit()

    return update_query.first()


@router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_model=None)
async def delete_todid(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ) -> None:
    delete_query = db.query(Todid).filter(Todid.id == id)
    todid = delete_query.first()
    if not todid:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"ToDid with id '{id}' was not found." )

    # Validate the user owns the todid item
    if todid.createdBy != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
