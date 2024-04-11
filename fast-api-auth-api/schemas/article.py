from typing import Optional

from pydantic import BaseModel, HttpUrl


class Article(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    source_url: HttpUrl
    author_id: Optional[int]

    class Config:
        orm_mode = True