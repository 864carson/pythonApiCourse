from passlib.context import CryptContext

# Creates a CryptContext object for password hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    """
    The function `hash` takes a password as input and returns its hashed value using a password hashing
    context.

    :param password: A password as a string.
    :type password: str

    :return: The hashed version of the input `password` string using the `pwd_context` hashing algorithm.
    """

    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plain text password with a hashed password to determine if they match.

    :param plain_password: The password entered by the user in plain text, before it is hashed for security purposes.
    :type plain_password: str

    :param hashed_password: A string that represents the hashed version of a password. This hashed password is
    typically stored in a database or used for authentication purposes.
    :type hashed_password: str

    :return: A boolean value indicating whether the plain password matches the hashed password after verification.
    """

    return pwd_context.verify(plain_password, hashed_password)
