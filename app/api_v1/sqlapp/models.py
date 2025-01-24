import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, Text, VARCHAR, ForeignKey, Enum
from sqlalchemy.orm import relationship
from api_v1.sqlapp.database import Base



class FeedbackScore(enum.Enum):
    bad = 1
    norm = 2
    cool = 3


class UserTable(Base):
    __tablename__ = 'usertable'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    student_id = Column(Integer, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False)
    tg_id = Column(VARCHAR(length=32), unique=True)
    login = Column(VARCHAR(length=32), nullable=False, unique=True)
    password = Column(VARCHAR(length=64), nullable=False)
    name = Column(VARCHAR(length=32), nullable=False)
    sname = Column(VARCHAR(length=32), nullable=False)
    kpd_score = Column(Integer, nullable=False)

    role_id = Column(Integer, ForeignKey("roletable.id"))
    role = relationship("RoleTable", back_populates="users", lazy=False)

    room_id = Column(Integer, ForeignKey("roomtable.id"))
    room = relationship("RoomTable", back_populates="users", lazy=False)


class RoleTable(Base):
    __tablename__ = 'roletable'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(length=32), nullable=False)
    acsess_level = Column(Integer, nullable=False)
    users = relationship("UserTable", back_populates="role", lazy=False)


class RoomTable(Base):
    __tablename__ = 'roomtable'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(VARCHAR(length=8), nullable=False)

    users = relationship("UserTable", back_populates="room", lazy=False)


class EventTypeTable(Base):
    __tablename__ = 'eventtypetable'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(length=32), nullable=False)


class ImageTable(Base):
    __tablename__ = 'imagetable'
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(VARCHAR(length=256), nullable=False)

    event_id = Column(Integer, ForeignKey("eventlogtable.id"))
    event = relationship("EventLogTable", back_populates="images", lazy=False)


class EventLogTable(Base):
    __tablename__ = 'eventlogtable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    message = Column(Text, nullable=False)
    kpd_diff = Column(Integer, nullable=False)

    event_target_id = Column(Integer)
    event_initiator_id = Column(Integer, ForeignKey("usertable.id"))

    event_type_id = Column(Integer, ForeignKey("eventtypetable.id"))
    images = relationship("ImageTable", back_populates="event", lazy=False)


class NotificationTable(Base):
    __tablename__ = 'notificationtable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    event_date = Column(TIMESTAMP, default=datetime.utcnow)
    remind_hours = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    is_notificated = Column(Boolean, nullable=False)

    initiator_id = Column(Integer, ForeignKey("usertable.id"))


class FeedbackTable(Base):
    __tablename__ = 'feedbacktable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    message = Column(Text, nullable=False)
    feedback_score = Column(Integer, nullable=False)

    initiator_id = Column(Integer, ForeignKey("usertable.id"))


class SankomTable(Base):
    __tablename__ = 'sankomtable'

    id = Column(Integer, primary_key=True)
    mark = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    initiator_id = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('usertable.id'))
    user = relationship("UserTable", lazy=False)

class WorkTicketTable(Base):
    __tablename__ = 'worktickettable'

    id = Column(Integer, primary_key=True)
    deadline = Column(TIMESTAMP, nullable=False)
    kpd_rollback = Column(Integer, nullable=False)
    ticket_hash = Column(String(256), nullable=False)
    text_task = Column(Text, nullable=False)

    performer_id = Column(Integer, ForeignKey('usertable.id'))
    performer = relationship("UserTable", lazy=False)