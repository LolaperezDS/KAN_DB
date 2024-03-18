from pydantic import BaseModel


class UserGet(BaseModel):
    name: str
    sname: str
    kpd: int
    role : str
    stud_id: int
    room: str
