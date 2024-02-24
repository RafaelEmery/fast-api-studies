from typing import Optional

from pydantic import BaseModel


class CourseSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    author_name: str
    classes: int
    hours: int
    is_active: Optional[bool] = True

    class Config:
        # This will allow the Pydantic model to work with SQLAlchemy ORM models
        from_attributes = True