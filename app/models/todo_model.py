from typing import Optional
from pydantic import BaseModel

# Define the Todo model with pydantic
class TodoModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: Optional[int] = None
    label: Optional[str] = None
    parent: Optional[object] = None
    # remind: Optional[datetime] = None
    # due: Optional[datetime] = None
