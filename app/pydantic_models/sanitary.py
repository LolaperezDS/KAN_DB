from pydantic import BaseModel, ConfigDict
from datetime import datetime

# from users import UserGet

class SanitaryMarkCreate(BaseModel):
    room_id: int
    mark: int


class SanitaryMarkGet(SanitaryMarkCreate):
    date: datetime
    created_by: int
