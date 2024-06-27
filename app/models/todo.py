from sqlalchemy import Column, Integer, String, Text, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database import Base


# Define the Todo model with SQLAlchemy
class Todo(Base):
    __tablename__ = "Todos"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(length=512), nullable=False, index=True)
    description = Column(Text, nullable=True)
    createdOn = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    updatedOn = Column(TIMESTAMP(timezone=True), nullable=True)
    # priority: Optional[int] = None
    # label: Optional[str] = None
    # parent: Optional[object] = None
    # remind: Optional[datetime] = None
    # due: Optional[datetime] = None
