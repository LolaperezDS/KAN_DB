from sql_app.models.models import UserTable, EventLogTable, NotificationTable, FeedbackTable, FeedbackScore


def get_user_by_tg_id(tg_id: int, session) -> UserTable:
    try:
        user = session.query(UserTable).filter(UserTable.tg_id == str(tg_id)).first()
        return user
    except Exception as e:
        session.rollback()
        raise e

def get_user_by_name(name: str, sname: str, session) -> UserTable:
    try:
        user = session.query(UserTable).filter(UserTable.name == name and UserTable.sname == sname).first()
        return user
    except Exception as e:
        session.rollback()
        raise e

# Получение всех пользователей чьи кпд > 0 (доступ только у модераторов)
def get_users_with_positive_kpd(current_user: UserTable, session) -> [UserTable]:
    if (current_user.role.acsess_level < 2):
        return None
    try:
        users = session.query(UserTable).filter(UserTable.role.acsess_level < 3, UserTable.kpd_score > 0).all()
        return users
    except Exception as e:
        session.rollback()
        raise e

# Отмена всех уведомлений (доступ только у администратора)
def cancel_all_notifications(current_user: UserTable, session) -> None:
    if current_user.role.acsess_level < 3:
        return
    try:
        session.query(NotificationTable).update({NotificationTable.is_notificated: True})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


# Создание фидбека (доступ только у пользователя)
def create_feedback(feedback: FeedbackTable, session):
    try:
        session.add(feedback)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


# Смена своего пароля после авторизации
def change_password(new_password: str, current_user: UserTable, session):
    try:
        user = session.query(UserTable).filter(UserTable.id == current_user.id).first()
        user.password = new_password
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        return False


# Деаутентификация со всех аккаунтов после авторизации
def deauthenticate(current_user: UserTable, session) -> bool:
    try:
        current_user.tg_id = None
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        return False


# Авторизация (привязка ID после ввода пароля)
def authenticate(tg_id: int, login: str, password: str, session) -> bool:
    try:
        user = session.query(UserTable).filter(UserTable.password == password and UserTable.login == login).first()
        if user is None:
            return False

        user.tg_id = str(tg_id)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        return False


def get_tg_id_all_users(session) -> [str]:
    try:
        users = session.query(UserTable).filter(UserTable.role.acsess_level <= 2).filter(UserTable.tg_id is not None).all()
        user_ids = [user.tg_id for user in users]
        return user_ids
    except Exception as e:
        session.rollback()
        raise e


def get_all_not_notified(session):
    try:
        ntf = session.query(NotificationTable).filter(NotificationTable.is_notificated == False).all()
        return ntf
    except Exception as e:
        raise e


def cancel_notification_by_id(id, session):
    try:
        ntf = session.query(NotificationTable).filter(NotificationTable.id == id).first()
        ntf.is_notificated = True
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def get_event_by_event_target_id(user: UserTable, count: int, session):
    try:
        if count < 1 or count > 50:
            return
        events = session.query(EventLogTable).filter(EventLogTable.event_target_id == user.id).limit(count)
    except Exception as e:
        session.rollback()
        raise e


def get_all_not_notified(session) -> [NotificationTable]:
    try:
        return session.query(NotificationTable).filter(not NotificationTable.is_notificated)
    except Exception as e:
        session.rollback()
        raise e