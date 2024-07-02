from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TodidSchemaBase(BaseModel):
    title: str
    description: Optional[str] | None = None

    class Config:
        orm_mode: True


class TodidSchemaCreate(TodidSchemaBase):
    pass


class TodidSchemaResponse(TodidSchemaBase):
    id: int
    createdOn: datetime
    updatedOn: datetime | None = None