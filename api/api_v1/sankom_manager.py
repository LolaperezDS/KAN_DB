from typing import List
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sqlapp.database import *
from api_v1.sqlapp.crud import *

from pydantic_models.users import *
from pydantic_models.kpd import *
from pydantic_models.sanitary import *

from .auth import get_current_active_user
from .user_manager import check_acsess_level


router = APIRouter(tags=['Sanitary'])


@router.get("/room/get/{room_name}")
async def get_room(room_name: str,
                   current_user : Annotated[UserTable, Depends(get_current_active_user)],
                   session: Annotated[AsyncSession, Depends(get_scoped_session)]) -> int:
    if not check_acsess_level(current_user, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    if len(room_name) != 4 or not (room_name[:3:].isdigit() and room_name[3].isalpha):
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="Неправильная сигнатура комнаты\n regex: %d%d%d%c"
        )
    room: RoomTable = await get_room_by_name(room_name, session=session)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Комната не найдена"
        )
    return room.id



@router.post("/mark/set")
async def set_mark(data: SanitaryMarkCreate,
                  current_user : Annotated[UserTable, Depends(get_current_active_user)],
                  session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    if not check_acsess_level(current_user, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    

    # Авто кпд при хреновых оценках (логику обсудить с наилем)