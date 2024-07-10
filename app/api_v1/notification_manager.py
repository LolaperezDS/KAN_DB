from typing import List
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sqlapp.database import *
from api_v1.sqlapp.crud import *

from pydantic_models.notification import *

from .auth import get_current_active_user
from .user_manager import check_acsess_level

router = APIRouter(tags=['Notification'])


def cast_bd_notify_to_pd(n: list[NotificationTable]) -> list[NotificationGet]:
    pd_notifications: list[NotificationGet] = []
    for notification in n:
        pd_notifications.append(NotificationGet(message=notification.message,
                                                remind_hours=notification.remind_hours,
                                                created_at=notification.created_at,
                                                event_date=notification.event_date,
                                                n_id=notification.id,
                                                initiator_id=notification.initiator_id,
                                                is_notificated=notification.is_notificated))
    return pd_notifications


@router.get("/all_not_notified", response_model=list[NotificationGet])
async def get_all_not_notified(current_user : Annotated[UserTable, Depends(get_current_active_user)],
                               session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    if not check_acsess_level(current_user, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    notifications: list[NotificationTable] = await get_notifications_all_not_notified(session=session)
    return cast_bd_notify_to_pd(notifications)


@router.get("/by_event_release_timestamp/start/{start}/end/{end}", response_model=list[NotificationGet])
async def get_by_event_release_timestamp(start: datetime,
                                         end: datetime,
                                         current_user : Annotated[UserTable, Depends(get_current_active_user)],
                                         session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    print("test")
    if not check_acsess_level(current_user, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    notifications: list[NotificationTable] = await get_notifications_by_event_release_timestamp(start=start,
                                                                                          end=end,
                                                                                          session=session)
    return cast_bd_notify_to_pd(notifications)


@router.post("/create")
async def create_notification(data: NotificationCreate,
                              current_user : Annotated[UserTable, Depends(get_current_active_user)],
                              session: Annotated[AsyncSession, Depends(get_scoped_session)]):
    if not check_acsess_level(current_user, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="доступ к выполнению запрещен"
        )
    await create_notification_by_data(NotificationTable(initiator_id=current_user.id,
                                                        event_date=data.event_date,
                                                        remind_hours=data.remind_hours,
                                                        message=data.message),
                                      session=session)