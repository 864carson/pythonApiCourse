from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session

# Creates an instance of the `OAuth2PasswordBearer` class from the `fastapi.security` module. This instance
# represents a scheme for handling OAuth2 password flow authentication in FastAPI.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiration


def create_access_token(data: dict):
    """
    Generates a JWT access token with an expiration time based on input data.

    :param data: A dictionary containing the information that you want to encode into the access token.
    This data could include user information, permissions, or any other relevant details that you want to
    associate with the token.
    :type data: dict

    :return: A JSON Web Token (JWT) that has been encoded using the data provided, a secret key,
    and a specified algorithm.
    """
    # make a copy of the data
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    """
    Decodes a JWT token using a secret key and algorithm, retrieves the user ID from the token payload,
    and returns a `TokenData` object with the user ID if it exists, otherwise raises a credentials exception.

    :param token: A string representing an access token that needs to be verified
    :type token: str

    :param credentials_exception: Likely an exception that is raised when there is an issue with the user's
    credentials or access token. It is used here to handle authentication errors. When an error occurs during the
    decoding of the access token or if the user_id is invalid.

    :return: An instance of `TokenData` with the `id` attribute set to the user ID extracted from the
    decoded JWT token payload.
    """

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
    """
    Retrieves the current user based on the provided access token and database session.

    :param token: A string representing the access token obtained from the OAuth2 authentication process.
    It is used to authenticate and authorize the user making the request.
    :type token: str

    :param db: An object of type `Session` obtained by calling the `get_db` dependency. This parameter represents
    a database session that will be used to query the database for the current user based on the provided access token.
    :type db: Session

    :return: The user object from the database whose ID matches the ID extracted from the access token.
    """

    # Create the exception that MAY be thrown later
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    # Return the user
    return db.query(User).filter(User.id == token.id).first()
