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
            detail="Неправильная сигнатура комнаты\n regex: %d%d%d%c\nExamples: 999L, 888S"
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
    mark: SankomTable = SankomTable(user_id=data.target_id,
                                    initiator_id=current_user.id,
                                    mark=data.mark)
    await create_mark(mark=mark,
                      session=session)
    return status.HTTP_200_OK


@router.get("mark/get/{stud_id}")
async def get_marks(stud_id: int,
                    current_user : Annotated[UserTable, Depends(get_current_active_user)],
                    session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    if not check_acsess_level(current_user, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    return [SanitaryMarkGet(target_id=mark.user_id,
                            mark=mark.mark,
                            created_by=mark.initiator_id,
                            date=mark.created_at) for mark in await get_last_marks(user_id=stud_id, session=session)]


@router.get("mark/my")
async def get_marks(current_user : Annotated[UserTable, Depends(get_current_active_user)],
                    session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    return [SanitaryMarkGet(target_id=mark.user_id,
                            mark=mark.mark,
                            created_by=mark.initiator_id,
                            date=mark.created_at) for mark in await get_last_marks(user_id=current_user.id, session=session)]


@router.get("mark/roomusers/{room_id}")
async def get_roomusers(room_id: int,
                         current_user : Annotated[UserTable, Depends(get_current_active_user)],
                         session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    if not check_acsess_level(current_user, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    return [UserGet(stud_id=user.id,
                    name=user.name,
                    sname=user.sname,
                    room=user.room.number,
                    kpd=user.kpd_score,
                    role=None) for user in await get_room_users(room_id=room_id, session=session)]

