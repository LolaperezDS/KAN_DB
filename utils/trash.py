from sql_app.models.models import UserTable, FeedbackScore, NotificationTable, EventLogTable, FeedbackTable

from sql_app.utils.crud import create_user, update_user, delete_user, get_all_users, \
    get_own_profile_by_tg_id, create_event, get_event_by_id, get_event_by_event_target_id, \
    get_users_with_positive_kpd, cancel_all_notifications, delete_notification, update_notification, \
    create_notification, read_feedback, \
    create_feedback, force_change_password, change_password, deauthenticate, authenticate

from sql_app.database.database import SessionLocal, engine

from datetime import datetime, timedelta

session = SessionLocal(bind=engine)

common_user = UserTable(id=3,
                        is_active=True,
                        tg_id="2",
                        password="2",
                        full_name="2",
                        kpd_score=2,
                        role_id=3)

user_data = {
    'is_active': True,
    'tg_id': None,
    'password': '123',
    'full_name': 'amir',
    'kpd_score': 100,
    'role_id': 2
}
session.query(EventLogTable).delete()
session.query(UserTable).delete()
session.query(NotificationTable).delete()
session.query(FeedbackTable).delete()
session.commit()
"""
Габитов Данил Димович @Da_da_nil 30
Хайруллов Нияз Ильдарович @Geravod 15
Каров Ярослав Сергеевич @source_number 0  
Самойлова Анастасия Олеговна @an_samoj1ova 45
Константинов Константин Николаевич @nihilnigdizm 75

"""

common_user1 = UserTable(id=None,
                        is_active=True,
                        tg_id=None,
                        login="Game_BEAT_Ich",
                        password="qwe",
                        full_name="Габитов Данил Димович",
                        kpd_score=150,
                        role_id=1)
common_user2 = UserTable(id=None,
                        is_active=True,
                        tg_id=None,
                        login="GOD",
                        password="zxc",
                        full_name="Каров Ярослав Сергеевич",
                        kpd_score=0,
                        role_id=3)

session.add(common_user1)
session.add(common_user2)
session.commit()

users = get_all_users(common_user, session)
for user in users:
    print(user.full_name, user.password, user.kpd_score, user.role_id, user.id)

events = session.query(EventLogTable).all()
for event in events:
    print(event.event_type, event.message, event.kpd_diff, event.event_target_id)

feedbacks = session.query(FeedbackTable).all()
for feedback in feedbacks:
    print(feedback.message)
"""
try:
    new_user = create_user(user_data=user_data, current_user=current_user, session=session)
    print(f"User {new_user} created successfully.")
except Exception as e:
    print(f"Failed to create user: {str(e)}")
finally:
    session.close()
"""