from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from app.database import get_db
from app.models.user import User
from app.schemas.auth import TokenData
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "e5edd906b79d913ad9698b554da178ea55d63db35765941901aeb8707a738b9ce07bc7ad3e43412197462a800f1920cbdba8da79d63ca4a191aea0928bed6a1dce7b1f3b73bb3efabd144ac7cc281a5ad0a6979ebf79d9085eef6e2292587a97172bb0b3c003a74180c9715b062b40c5abc482981bcee288b6c0baa209a9ea7c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240


def create_access_token(data: dict):
    # make a copy of the data
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        return TokenData(id=f"{user_id}")
    except JWTError:
        raise credentials_exception


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)):
    # Create the exception that MAY be thrown later
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    # Return the user
    return db.query(User).filter(User.id == token.id).first()
