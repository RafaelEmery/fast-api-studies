from typing import Optional

from sqlmodel import Field, SQLModel


# If table is False, you can use the model as a pydantic schema
class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    classes: int
    hours: int