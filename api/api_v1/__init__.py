from fastapi import APIRouter

from api_v1.auth import router as auth_router
from api_v1.user_manager import router as user_router

router = APIRouter()
router.include_router(router=user_router, prefix="/user")
router.include_router(router=auth_router, prefix="/login")

