from pydantic import BaseModel
from datetime import datetime


class NotificationCreate(BaseModel):
    message: str
    remind_hours: int
    event_date: datetime

    class Config:
        orm_mode = True


class NotificationGet(NotificationCreate):
    initiator_id: int
    n_id: int
    created_at: datetime
    is_notificated: bool


class Timestamp(BaseModel):
    start: datetime
    end: datetime
