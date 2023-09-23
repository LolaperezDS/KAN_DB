import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, Text, VARCHAR, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sql_app.database.database import engine
from sql_app.database.database import Base

from dotenv import load_dotenv
import os

load_dotenv()

IS_PRODUCTION_MODE = bool(int(os.environ.get("IS_PRODUCTION_MODE")))

Base.metadata.create_all(engine) if IS_PRODUCTION_MODE else print("DB not connected")


# Определяем типы обратной связи
class FeedbackScore(enum.Enum):
    bad = 1
    norm = 2
    cool = 3


"""
CREATE TABLE UserTable(
  id SERIAL PRIMARY KEY,
  is_active bool NOT NULL,
  tg_id VARCHAR(32) UNIQUE,
  login VARCHAR(32) NOT NULL UNIQUE,
  password VARCHAR(64) NOT NULL,
  name VARCHAR(32) NOT NULL,
  sname VARCHAR(32) NOT NULL,
  kpd_score integer NOT NULL
);

CREATE TABLE RoleTable(
  id SERIAL PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  acsess_level integer NOT NULL
);


CREATE TABLE FloorTable(
  id SERIAL PRIMARY KEY,
  number integer NOT NULL
);


CREATE TABLE RoomTable(
  id SERIAL PRIMARY KEY,
  number VARCHAR(8) NOT NULL
);


CREATE TABLE FeedbackTable(
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  message TEXT NOT NULL,
  feedback_score integer
);

CREATE TABLE EventTypeTable(
  id SERIAL PRIMARY KEY,
  name VARCHAR(32) NOT NULL
);

CREATE TABLE EventLogTable(
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  message TEXT NOT NULL,
  kpd_diff integer NOT NULL,
  event_target_id integer NOT NULL
);

CREATE TABLE ImageTable(
  id SERIAL PRIMARY KEY,
  image_id VARCHAR(128) NOT NULL
);

CREATE TABLE NotificationTable(
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  event_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  remind_hours integer NOT NULL,
  message TEXT NOT NULL,
  is_notificated bool NOT NULL DEFAULT FALSE
);

CREATE TABLE ThroughTable(
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_done bool NOT NULL DEFAULT FALSE
);


ALTER TABLE UserTable ADD role_id integer REFERENCES RoleTable(id);
ALTER TABLE UserTable ADD room_id integer REFERENCES RoomTable(id);
ALTER TABLE RoomTable ADD floor_id integer REFERENCES FloorTable(id);

ALTER TABLE FeedbackTable ADD initiator_id integer REFERENCES UserTable(id);
ALTER TABLE EventLogTable ADD event_initiator_id integer REFERENCES UserTable(id);
ALTER TABLE EventLogTable ADD event_type_id integer REFERENCES EventTypeTable(id);

ALTER TABLE NotificationTable ADD initiator_id integer REFERENCES UserTable(id);
ALTER TABLE ThroughTable ADD initiator_id integer REFERENCES UserTable(id);
ALTER TABLE ThroughTable ADD floor_id integer REFERENCES FloorTable(id);

"""


# Определяем модель для свойств пользователей
class UserTable(Base):
    __tablename__ = 'usertable'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False)
    tg_id = Column(VARCHAR(length=32), unique=True)
    login = Column(VARCHAR(length=32), nullable=False, unique=True)
    password = Column(VARCHAR(length=64), nullable=False)
    name = Column(VARCHAR(length=32), nullable=False)
    sname = Column(VARCHAR(length=32), nullable=False)
    kpd_score = Column(Integer, nullable=False)

    role_id = Column(Integer, ForeignKey("roletable.id"))
    role = relationship("RoleTable", back_populates="users")

    room_id = Column(Integer, ForeignKey("roomtable.id"))
    room = relationship("RoomTable", back_populates="users")


# Определяем модель для привилегий пользователей
class RoleTable(Base):
    __tablename__ = 'roletable'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(length=32), nullable=False)
    acsess_level = Column(Integer, nullable=False)
    users = relationship("UserTable", back_populates="role")


class RoomTable(Base):
    __tablename__ = 'roomtable'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)

    users = relationship("UserTable", back_populates="room")

    floor_id = Column(Integer, ForeignKey("floortable.id"))
    floor = relationship("FloorTable", back_populates="rooms")


class FloorTable(Base):
    __tablename__ = 'floortable'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    rooms = relationship("RoomTable", back_populates="floor")


class EventTypeTable(Base):
    __tablename__ = 'eventtypetable'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(length=32), nullable=False)


class ImageTable(Base):
    __tablename__ = 'imagetable'
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(VARCHAR(length=128), nullable=False)

    event_id = Column(Integer, ForeignKey("eventlogtable.id"))
    event = relationship("EventLogTable", back_populates="images")


# Определяем модель для событий
class EventLogTable(Base):
    __tablename__ = 'eventlogtable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    message = Column(Text, nullable=False)
    kpd_diff = Column(Integer, nullable=False)

    event_target_id = Column(Integer)
    event_initiator_id = Column(Integer, ForeignKey("usertable.id"))

    event_type_id = Column(Integer, ForeignKey("eventtypetable.id"))
    images = relationship("ImageTable", back_populates="event")


# Определяем модель для уведомлений
class NotificationTable(Base):
    __tablename__ = 'notificationtable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    event_date = Column(TIMESTAMP, default=datetime.utcnow)
    remind_hours = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    is_notificated = Column(Boolean, nullable=False)

    initiator_id = Column(Integer, ForeignKey("usertable.id"))


# Определяем модель для обратной связи
class FeedbackTable(Base):
    __tablename__ = 'feedbacktable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    message = Column(Text, nullable=False)
    feedback_score = Column(Integer, nullable=False)

    initiator_id = Column(Integer, ForeignKey("usertable.id"))


class ThroughTable(Base):
    __tablename__ = 'throughtable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, nullable=False)

    initiator_id = Column(Integer, ForeignKey("usertable.id"))
    floor_id = Column(Integer, ForeignKey("floortable.id"))


