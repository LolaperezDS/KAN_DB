from typing import List
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sqlapp.database import *
from api_v1.sqlapp.crud import *

from pydantic_models.users import *

from .auth import get_current_active_user
from service import pwd_functions


router = APIRouter(tags=['UserManage'])


def check_acsess_level(User: UserTable, level: int) -> bool:
    return level <= User.role.acsess_level


@router.get("/me", response_model=UserGet)
async def get_myself(current_user : Annotated[UserTable, Depends(get_current_active_user)]):
    pd_user = UserGet(name=current_user.name,
                      sname=current_user.sname,
                      kpd=current_user.kpd_score,
                      role=current_user.role.name,
                      stud_id=current_user.student_id,
                      room=current_user.room.number)
    return pd_user


@router.post("/create/{name}/{sname}/{stud_id}/{room}")
async def post_create_user(name: str,
                      sname: str,
                      stud_id: int,
                      room_name: str,
                      current_user : Annotated[UserTable, Depends(get_current_active_user)],
                      session: Annotated[AsyncSession, Depends(get_scoped_session)],
                      role_id: int = 1,
                      tg_id: str | None = None,
                      kpd_score: int = 0,
                      login : str | None = None,
                      password: str | None = None):
    if not check_acsess_level(current_user, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    
    room: RoomTable = await get_room_by_name(room_name, session=session)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Комната не найдена"
        )
    
    if not login:
        login = pwd_functions.get_random_string(8)
    if not password:
        password = pwd_functions.get_random_string(52)  # LOL :)
    
    user: UserTable = UserTable(name=name,
                                sname=sname,
                                student_id=stud_id,
                                room_id=room.id,
                                role_id=role_id,
                                kpd_score=kpd_score,
                                is_active=True,
                                tg_id=tg_id,
                                login=login,
                                password=password)
    await create_user(user, session)


# Переменная activate управляет состоянием is_active в бд после запроса
@router.post("/switch/active/{stud_id}/{activate}")
async def post_user_deactivate():
    pass
