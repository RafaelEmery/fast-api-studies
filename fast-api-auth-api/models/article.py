from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class Article(settings.DBBaseModel):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(length=256), unique=True)
    content = Column(String)
    source_url = Column(String(256))
    author_id = Column(Integer, ForeignKey("users.id"))

    """
    back_populates information at https://stackoverflow.com/questions/39869793/when-do-i-need-to-use-sqlalchemy-back-populates
    lazy information at https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html
    """
    author = relationship("User", back_populates="articles", lazy="joined")
