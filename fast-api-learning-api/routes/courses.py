from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from db import fake_db
from models import Course, courses

router = APIRouter()

@router.get("/api/v1/courses", description="Get all courses", response_model=list[Course])
async def get_courses(db: Any = Depends(fake_db)):
    return courses

@router.post("/api/v1/courses", description="Create course", response_model=Course)
async def create_course(course: Course, db: Any = Depends(fake_db)):
    next_id: int = len(courses) + 1
    course.id = next_id
    courses.append(course)
    
    return courses[next_id]