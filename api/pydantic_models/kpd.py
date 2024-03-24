from pydantic import BaseModel
from datetime import datetime

class ImageType(BaseModel):
    data: str


class Kpd(BaseModel):
    message: str
    kpd_diff: int
    target_stud_id: int
    images: list[ImageType]

    class Config:
        orm_mode = True



class KpdGet(Kpd):
    target_stud_id: int | None
    initiator_id: int
    date: datetime
