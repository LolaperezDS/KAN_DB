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
  tg_id VARCHAR(50) UNIQUE,
  password TEXT NOT NULL,
  full_name TEXT NOT NULL,
  kpd_score integer NOT NULL
);

CREATE TABLE RoleTable(
  id SERIAL PRIMARY KEY,
  privilege TEXT
);

CREATE TABLE EventLogTable(
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  event_type TEXT NOT NULL,
  message TEXT NOT NULL,
  kpd_diff integer NOT NULL,
  event_target_id integer NOT NULL
);


CREATE TABLE NotificationTable(
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  event_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  remind_hours integer NOT NULL,
  message TEXT NOT NULL,
  is_notificated bool NOT NULL DEFAULT FALSE
);


CREATE TABLE FeedbackTable(
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  message TEXT NOT NULL,
  feedback_score integer
);


ALTER TABLE UserTable ADD role_id integer REFERENCES roletable(id);
ALTER TABLE EventLogTable ADD event_initiator_id integer REFERENCES UserTable(id);
ALTER TABLE NotificationTable ADD initiator_id integer REFERENCES UserTable(id);
ALTER TABLE FeedbackTable ADD user_id integer REFERENCES UserTable(id);
"""


# Определяем модель для свойств пользователей
class UserTable(Base):
    __tablename__ = 'usertable'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False)
    tg_id = Column(VARCHAR(length=50), unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    kpd_score = Column(Integer, nullable=False)

    role_id = Column(Integer, ForeignKey("roletable.id"))
    role = relationship("RoleTable", foreign_keys=[role_id])


# Определяем модель для привилегий пользователей
class RoleTable(Base):
    __tablename__ = 'roletable'
    id = Column(Integer, primary_key=True, index=True)
    privilege = Column(String, index=True)



# Определяем модель для событий
class EventLogTable(Base):
    __tablename__ = 'eventlogtable'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    event_type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    kpd_diff = Column(Integer, nullable=False)

    event_target_id = Column(Integer)
    event_initiator_id = Column(Integer, ForeignKey("usertable.id"))


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
    feedback_score = Column(Enum(FeedbackScore))

    user_id = Column(Integer, ForeignKey("usertable.id"))
