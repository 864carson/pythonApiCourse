from sqlalchemy import Column, Integer, String, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(length=256), nullable=False, unique=True, index=True)
    password = Column(String(128), nullable=False)
    createdOn = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    updatedOn = Column(TIMESTAMP(timezone=True), nullable=True)
