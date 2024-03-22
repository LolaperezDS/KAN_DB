from pydantic import BaseModel
from datetime import datetime

class ImageType(BaseModel):
    data: str
    kpd_id: int


class Kpd(BaseModel):
    message: str
    kpd_diff: int
    target_id: int
    images: list[ImageType]


class KpdGet(Kpd):
    initiator_id: int
    date: datetime