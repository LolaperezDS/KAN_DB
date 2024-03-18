from typing import List
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sqlapp.database import *
from api_v1.sqlapp.crud import *

from pydantic_models.users import *

from .auth import get_current_active_user


router = APIRouter(tags=['UserManage'])

@router.get("/me")
async def get_myself(current_user : Annotated[UserTable, Depends(get_current_active_user)]):
    pd_user = UserGet(name=current_user.name,
                      sname=current_user.sname,
                      kpd=current_user.kpd_score,
                      role=current_user.role.name,
                      stud_id=current_user.student_id,
                      room=current_user.room.number)
    return pd_user
