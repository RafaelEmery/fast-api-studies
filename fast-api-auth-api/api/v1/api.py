from fastapi import APIRouter
from api.v1.endpoints import user, article


router = APIRouter()


router.include_router(user.router, prefix='/users', tags=['User'])
router.include_router(article.router, prefix='/articles', tags=['Article'])