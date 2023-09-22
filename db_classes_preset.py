
"""
sudo -u postgres psql -U postgres -d kan

INSERT INTO RoleTable (name, acsess_level) VALUES ('Student', 1);
INSERT INTO RoleTable (name, acsess_level) VALUES ('Moderator', 2);
INSERT INTO RoleTable (name, acsess_level) VALUES ('Admin', 3);
INSERT INTO EventTypeTable (name) VALUES ('sankom kpd');
INSERT INTO FloorTable (number) VALUES (3);
INSERT INTO RoomTable (number, floor_id) VALUES ('316b', 1);
INSERT INTO RoomTable (number, floor_id) VALUES ('302a', 1);

INSERT INTO UserTable (is_active, tg_id, login, password, name, sname, kpd_score, role_id, room_id)
VALUES (true, NULL, 'Invoker', 'qwe', 'Данил', 'Габитов', 150, 1, 1);
INSERT INTO UserTable (is_active, tg_id, login, password, name, sname, kpd_score, role_id, room_id)
VALUES (true, NULL, 'INSERT INTO UserTable (is_active, tg_id, login, password, name, sname, kpd_score, role_id, room_id)
VALUES (true, NULL, 'LoginTest', 'asd', 'Ivan', 'Ivanich', 15, 3, 2);
ShadowFiend', 'zxc', 'Yarik', 'Karov', 0, 2, 1);
"""