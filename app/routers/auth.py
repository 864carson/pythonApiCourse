from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import oauth2, utils
from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token


router = APIRouter(tags=["Authentication Endpoints"])


@router.post(
    "/login",
    response_model=Token
)
async def login(credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.username).first()
    if not user:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials")

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials")

    # Create and return token
    token = oauth2.create_access_token(data={"user_id":user.id})
    return { "access_token": token, "token_type": "bearer" }
