from typing import Optional
from pydantic import BaseModel

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int 
    hours: int

    @validator("title")
    def validate_title(cls, value: str):
        if len(value) < 5:
            raise ValueError("Title must be at least 5 characters long")
        words = value.split(" ")
        if len(words) < 3:
            raise ValueError("Title must have at least 3 words")
        return value

# Sample courses list
courses = [
    Course(id=1, title="first course", classes=10, hours=20),
    Course(id=2, title="second course", classes=5, hours=10),
    Course(id=3, title="third course", classes=20, hours=40),
    Course(id=4, title="fourth course", classes=15, hours=30)
]

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str

users = [
    User(id=1, username="user1", email="", password=""),
    User(id=1, username="user2", email="", password=""),
    User(id=3, username="user3", email="", password=""),
]


