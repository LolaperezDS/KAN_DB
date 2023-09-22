from sql_app.models.models import UserTable, FeedbackScore, NotificationTable, EventLogTable, FeedbackTable, ImageTable, RoomTable, RoleTable, FloorTable, EventTypeTable, ThroughTable

from sql_app.database.database import SessionLocal, engine

from db_classes_preset import *

session = SessionLocal(bind=engine)

# Clearing
session.query(EventLogTable).delete()
session.query(EventTypeTable).delete()
session.query(FeedbackScore).delete()
session.query(ImageTable).delete()
session.query(RoleTable).delete()
session.query(UserTable).delete()
session.query(NotificationTable).delete()
session.query(FeedbackTable).delete()
session.query(RoomTable).delete()
session.query(ThroughTable).delete()
session.query(FloorTable).delete()
session.commit()

#AddingData
session.add_all([event1, floor, room1, room2, role1, role2, role3,
                  common_user1, common_user2, common_user3])
session.commit()

