from fastapi import Depends, status, HTTPException, APIRouter
from app import utils
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserSchemaCreate, UserSchemaResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["User Endpoints"])

@router.get(
        "/",
        response_model=list[UserSchemaResponse],
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_users(db: Session = Depends(get_db)) -> list[UserSchemaResponse]:
    users = db.query(User).all()
    return users


@router.get("/{id}",
        response_model=UserSchemaResponse,
        response_model_exclude_unset=True,
        response_model_exclude_none=True)
async def get_user(id: int, db: Session = Depends(get_db)) -> UserSchemaResponse:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' was not found." )

    return user


@router.post(
        "/",
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
