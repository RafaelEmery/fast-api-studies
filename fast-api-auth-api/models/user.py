from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings


class User(settings.DBBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(length=256))
    last_name = Column(String(length=256))
    email = Column(String(length=256), index=True, nullable=False, unique=True)
    password = Column(String(length=256), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    articles = relationship("Article", cascade="all,delete-orphan", back_populates="author", uselist=True,lazy="joined")
