from fastapi import APIRouter, Depends
from typing import Any

from db import fake_db
from models import User, users

router = APIRouter()

@router.get("/api/v1/users", description="Get all users", response_model=list[User])
async def get_courses(db: Any = Depends(fake_db)):
    return users