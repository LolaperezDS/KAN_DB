from typing import List
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sqlapp.database import *
from api_v1.sqlapp.crud import *

from pydantic_models.users import *
from pydantic_models.kpd import *

from .auth import get_current_active_user
from .user_manager import check_acsess_level

router = APIRouter(tags=['KpdManage'])


@router.get("/my/all", response_model=list[KpdGet])
async def get_my_kpd():
    pass


@router.post("/set")
async def get_my_kpd(data: Kpd,
                     current_user : Annotated[UserTable, Depends(get_current_active_user)],
                     session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    pass



"""
[ ] - My KPD
[ ] - Other KPD
[ ] - Set KPD
[ ] - list KPD > 0
"""