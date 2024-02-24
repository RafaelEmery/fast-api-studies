from core.configs import settings

from sqlalchemy import Column, Integer, String, Boolean


class Course(settings.DBBaseModel):
    __tablename__ = 'courses'

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title: str = Column(String(100), nullable=False)
    description: str = Column(String, nullable=True)
    author_name: str = Column(String(50), nullable=False)
    classes: int = Column(Integer, nullable=False)
    hours: int = Column(Integer, nullable=False)
    is_active: bool = Column(Boolean, default=True)