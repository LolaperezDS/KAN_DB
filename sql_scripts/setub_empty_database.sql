DROP DATABASE kandb;
CREATE DATABASE kandb;

\c kandb

CREATE TABLE UserTable(
  id SERIAL PRIMARY KEY,
  student_id integer UNIQUE NOT NULL,
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


ALTER TABLE UserTable ADD role_id integer REFERENCES RoleTable(id);
ALTER TABLE UserTable ADD room_id integer REFERENCES RoomTable(id);

ALTER TABLE FeedbackTable ADD initiator_id integer REFERENCES UserTable(id);
ALTER TABLE EventLogTable ADD event_initiator_id integer REFERENCES UserTable(id);
ALTER TABLE EventLogTable ADD event_type_id integer REFERENCES EventTypeTable(id);

ALTER TABLE NotificationTable ADD initiator_id integer REFERENCES UserTable(id);
ALTER TABLE ImageTable ADD event_id integer REFERENCES EventLogTable(id);

INSERT INTO RoleTable (name, acsess_level) VALUES ('Student', 1);
INSERT INTO RoleTable (name, acsess_level) VALUES ('Moderator', 2);
INSERT INTO RoleTable (name, acsess_level) VALUES ('Admin', 3);

INSERT INTO EventTypeTable (name) VALUES ('sankom kpd');
INSERT INTO EventTypeTable (name) VALUES ('gro kpd');