from sqlalchemy import Column, BigInteger, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base


# Define the ToDid model with SQLAlchemy
class Todid(Base):
    __tablename__ = "todids"

    id = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(String(length=512), nullable=False, index=True)
    description = Column(Text, nullable=True)
    createdBy = Column(Integer, ForeignKey("users.id", ondelete="No Action"), nullable=False)
    createdByName = relationship("User")
    createdOn = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    updatedOn = Column(TIMESTAMP(timezone=True), nullable=True)
