from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:car04soN!30$@localhost/ToDid'

# Creates a database engine using SQLAlchemy. The `create_engine` function is used to create an engine object that
# represents a connection to the database specified in the `SQLALCHEMY_DATABASE_URL`. This engine will be used to
# interact with the database, such as executing queries and managing connections.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creates a session factory that will be used to create database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All models must extend this base class
Base = declarative_base()


def get_db():
    """
    Creates a database session and yields it for use, ensuring the session is closed properly afterwards.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
