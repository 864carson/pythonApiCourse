from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserSchemaResponse


class TodidSchemaBase(BaseModel):
    title: str
    description: Optional[str] | None = None

    class Config:
        orm_mode: True


class TodidSchemaCreate(TodidSchemaBase):
    pass


class TodidSchemaResponse(TodidSchemaBase):
    id: int
    createdByName: UserSchemaResponse
    createdOn: datetime
    updatedOn: datetime | None = None
