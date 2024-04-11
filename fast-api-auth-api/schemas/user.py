from typing import Optional, List

from pydantic import BaseModel, EmailStr

from schemas.article import Article


class BaseUser(BaseModel):
    id: Optional[int]
    name: str
    last_name: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True


# Inherit from BaseUser then has all the attributes
class UserCreate(BaseUser):
    password: str


class UserArticles(BaseUser):
    articles: Optional[List[Article]]


class UserUpdate(BaseUser):
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_admin: Optional[bool]