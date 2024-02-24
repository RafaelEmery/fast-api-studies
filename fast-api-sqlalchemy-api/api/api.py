from fastapi import APIRouter

from api.v1.endpoints import course

router = APIRouter()
router.include_router(course.router, prefix="/courses", tags=["courses"])