from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TodoSchemaBase(BaseModel):
    title: str
    description: Optional[str] | None = None

    class Config:
        orm_mode: True


class TodoSchemaCreate(TodoSchemaBase):
    pass


class TodoSchemaResponse(TodoSchemaBase):
    id: int
    createdOn: datetime
    updatedOn: datetime | None = None