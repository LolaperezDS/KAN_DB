from fastapi import APIRouter

from api_v1.auth import router as auth_router
from api_v1.user_manager import router as user_router
from api_v1.kpd_manager import router as kpd_router
from api_v1.sankom_manager import router as sankom_router
from api_v1.notification_manager import router as notification_router

router = APIRouter()

router.include_router(router=user_router, prefix="/user")
router.include_router(router=auth_router, prefix="/login")
router.include_router(router=kpd_router, prefix="/kpd")
router.include_router(router=sankom_router, prefix="/sanitary")
router.include_router(router=notification_router, prefix="/notification")
