from sqlalchemy.exc import IntegrityError

from api_v1.sqlapp.models import *
from api_v1.sqlapp.database import *
from service.pwd_functions import verify_password
from sqlalchemy import select


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
        raise IntegrityError("The user is already stored")

async def get_room_by_name(name: str,
                           session: AsyncSession) -> RoomTable | None:
    room = (await session.execute(select(RoomTable).where(RoomTable.number == name))).unique().scalar_one_or_none()
    if not room:
        return None
    return room