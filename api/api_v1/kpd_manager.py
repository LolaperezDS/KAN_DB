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
async def get_my_kpd(current_user : Annotated[UserTable, Depends(get_current_active_user)],
                     session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    events: list[EventLogTable] = await get_all_kpd_by_id(current_user.id, session)


@router.post("/set")
async def set_kpd(data: Kpd,
                  current_user : Annotated[UserTable, Depends(get_current_active_user)],
                  session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    eventtype = None
    if data.kpd_diff <= 0 or len(data.message) < 5:
        eventtype = 6
    elif current_user.role.id == 4:
        eventtype = 3
    elif current_user.role.id == 5:
        eventtype = 4
    
    if not check_acsess_level(current_user, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    target: UserTable = get_user_by_internal_id(data.target_id, session=session)
    target = await target
    if not target:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь не найден"
        )
    target.kpd_score += data.kpd_diff
    await session.commit()
    
    event: EventLogTable = EventLogTable(message=data.message,
                                         kpd_diff=data.kpd_diff,
                                         event_target_id=data.target_id,
                                         event_initiator_id=current_user.id,
                                         event_type_id=eventtype)
    await create_kpd(event=event,
                     session=session)

    sql_images: list[ImageTable] = []
    for image_data in data.images:
        sql_images.append(ImageTable(event_id=event.id,
                                     image_id=image_data.data))
    
    await add_images_to_event(images=sql_images,
                              session=session)



"""

[ ] - My KPD
[ ] - Other KPD
[ ] - Set KPD
[ ] - list KPD > 0
"""