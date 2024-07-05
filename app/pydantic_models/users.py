from pydantic import BaseModel


class UserGet(BaseModel):
    name: str
    sname: str
    kpd: int
    role : str | None
    stud_id: int
    room: str


class UserCreate(BaseModel):
    name: str
    sname: str
    stud_id: int
    room: str
