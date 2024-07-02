from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserSchemaBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode: True


class UserSchemaCreate(UserSchemaBase):
    password: Optional[str] | None = None


class UserSchemaResponse(UserSchemaBase):
    id: int
    createdOn: datetime
    updatedOn: datetime | None = None
