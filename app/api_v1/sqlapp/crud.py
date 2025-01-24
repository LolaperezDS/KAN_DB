from sqlalchemy.exc import IntegrityError

from api_v1.sqlapp.models import *
from api_v1.sqlapp.database import *
from service.pwd_functions import verify_password
from sqlalchemy import select, update, delete


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = (await session.execute(select(UserTable).where(UserTable.login == username))).unique().scalar_one_or_none()

    if not user or not verify_password(password, user.password):
        return None
    return user

async def get_user(username: str,
                   session: AsyncSession) -> UserTable | None:
    statement = select(UserTable).where(UserTable.login == username)
    user = (await session.execute(statement)).unique().scalar_one_or_none()
    return user


async def create_user(user: UserTable,
                      session: AsyncSession) -> None:
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        raise ex("The user is already stored")

async def get_room_by_name(name: str,
                           session: AsyncSession) -> RoomTable | None:
    room = (await session.execute(select(RoomTable).where(RoomTable.number == name))).unique().scalar_one_or_none()
    if not room:
        return None
    return room


async def get_user_by_internal_id(id: int,
                                session: AsyncSession) -> UserTable | None:
    statement = select(UserTable).where(UserTable.id == id)
    user = (await session.execute(statement)).unique().scalar_one_or_none()
    return user


async def change_activity_user(activity: bool,
                                id: int,
                                session: AsyncSession) -> None:
    statement = update(UserTable).where(UserTable.id == id).values(is_active = activity)
    await session.execute(statement)
    await session.commit()


async def change_room_user(roomid: int,
                           id: int,
                           session: AsyncSession) -> None:
    statement = update(UserTable).where(UserTable.id == id).values(room_id = roomid)
    await session.execute(statement)
    await session.commit()


async def get_all_kpd_by_id(user_id: int, session: AsyncSession) -> list[EventLogTable]:
    statement = select(EventLogTable).where(EventLogTable.event_target_id == user_id)
    events = (await session.execute(statement=statement)).unique().scalars().all()
    return events

async def get_images_by_event_id(event_id: list[ImageTable],
                                session: AsyncSession) -> list[ImageTable]:
    statement = select(ImageTable).where(ImageTable.event_id == event_id)
    images = (await session.execute(statement=statement)).unique().scalars().all()
    return images


async def add_images_to_event(images: list[ImageTable],
                             session: AsyncSession) -> None:
    for image in images:
        session.add(image)
    try:
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        raise ex


async def create_kpd(event: EventLogTable,
                     session: AsyncSession):
    try:
        session.add(event)
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        raise ex


async def create_mark(mark: SankomTable,
                      session: AsyncSession):
    session.add(mark)
    try:
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        raise ex

async def create_notification_by_data(notification: NotificationTable,
                              session: AsyncSession) -> None:
    notification.is_notificated = False
    try:
        session.add(notification)
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        raise ex

async def get_notification_by_id(n_id: int,
                                session: AsyncSession) -> NotificationTable | None:
    notification = (await session.execute(select(NotificationTable).where(NotificationTable.id == n_id))).unique().scalar_one_or_none()
    return notification

async def get_notifications_all_not_notified(session: AsyncSession) -> list[NotificationTable]:
    notifications = (await session.execute(select(NotificationTable).where(NotificationTable.is_notificated == False))).unique().scalars().all()
    return notifications

async def get_notifications_by_event_release_timestamp(start: datetime,
                                          end: datetime,
                                          session: AsyncSession) -> list[NotificationTable]:
    # start, end = min(start, end), max(start, end)
    notifications = (await session.execute(select(NotificationTable).where(
                    NotificationTable.event_date >= start).where(
                    NotificationTable.event_date <= end))).unique().scalars().all()
    return notifications

async def get_last_marks(user_id: int,
                         session: AsyncSession,
                         count: int=None):
    marks = (await session.execute(select(SankomTable).where(UserTable.id == user_id))).unique().scalars().all()
    return marks
