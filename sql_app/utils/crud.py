from sql_app.models.models import UserTable, EventLogTable, NotificationTable, FeedbackTable, FeedbackScore


# Создание пользователя(доступ только у администратора)
def create_user(user_data, current_user, session) -> UserTable:
    if current_user.role_id != 1:
        raise Exception("Only admins can create users.")

    try:
        new_user = UserTable(**user_data)
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        session.rollback()
        raise e


# Изменение пользователя (доступ только у администратора)
def update_user(user_id, updated_user, current_user, session) -> UserTable:
    if current_user.role_id != 1:
        raise Exception("Only admins can update users.")

    try:
        user = session.query(UserTable).get(user_id)
        if user is None:
            raise Exception(f"User with ID {user_id} not found.")

        for key, value in updated_user.items():
            setattr(user, key, value)
        print(type(user))
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise e


# Удаление пользователя (доступ только у администратора)
def delete_user(user_id, current_user, session) -> bool:
    if current_user.role_id != 1:
        raise Exception("Only admins can delete users.")

    try:
        user = session.query(UserTable).get(user_id)
        if user is None:
            raise Exception(f"User with ID {user_id} not found.")

        session.delete(user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e


def get_user_by_tg_id(tg_id, session):
    try:
        user = session.query(UserTable).filter(UserTable.tg_id == tg_id).first()
        return user
    except Exception as e:
        session.rollback()
        raise e


def get_user_by_full_name(full_name, session):
    try:
        user = session.query(UserTable).filter(UserTable.full_name == full_name).first()
        return user
    except Exception as e:
        session.rollback()
        raise e

# Получение всех пользователей (доступ только у администраторов и модераторов)
def get_all_users(current_user, session) -> UserTable:
    if current_user.role_id != 1 and current_user.role_id != 2:
        # raise Exception("Only admins and moderators can get all users.")
        pass

    try:
        user = session.query(UserTable).all()
        return user
    except Exception as e:
        session.rollback()
        raise e


# Получение собственного профиля через тг айди (доступ у всех)
def get_own_profile_by_tg_id(tg_id, session) -> dict:
    try:
        user = session.query(UserTable).filter(UserTable.tg_id == tg_id).first()

        if user:
            profile = {
                'id': user.id,
                'tg_id': user.tg_id,
                'full_name': user.full_name,
                'kpd_score': user.kpd_score,
                'role': user.role.privilege
            }
            return profile
        else:
            raise Exception(f"User with TG ID '{tg_id}' not found.")
    except Exception as e:
        raise e


# Создание ивентов (доступ только у администраторов и модератов)
def create_event(event_data, subject_user, current_user, session) -> EventLogTable:
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise Exception("Only admins and moderators can create events.")

    try:
        new_event = EventLogTable()
        subj_user = get_user_by_full_name(subject_user, session)
        new_event.event_target_id = subj_user.id
        new_event.event_initiator_id = current_user.id
        new_event.event_type = event_data.get("event_type")
        new_event.message = event_data.get("message")
        new_event.kpd_diff = event_data.get("kpd_diff")
        setattr(subj_user, "kpd_score", subj_user.kpd_score + event_data.get("kpd_diff"))
        session.add(new_event)
        session.commit()
        return new_event
    except Exception as e:
        session.rollback()
        raise e


# Получение всех ивентов через айди (доступ только у администраторов и модератов)
def get_event_by_id(event_id, current_user, session) -> EventLogTable:
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise Exception("Only admins and moderators can get events by ID.")

    try:
        event = session.query(EventLogTable).get(event_id)
        return event
    except Exception as e:
        raise e


# Получение всех ивентов через айди человека, к которому этот ивент относится (доступ у всех)
def get_event_by_event_target_id(event_target_id, num_of_events: int, session):
    if num_of_events < 1 or num_of_events > 100:
        raise Exception("Incorrect num_of_events: ", num_of_events)
    try:
        events = session.query(EventLogTable).filter(EventLogTable.event_target_id == event_target_id).limit(num_of_events).all()
        return events
    except Exception as e:
        raise e


# Получение всех пользователей чьи кпд > 0 (доступ только у модераторов)
def get_users_with_positive_kpd(current_user, session):
    if not (current_user.role_id == 3 or current_user.role_id == 2):
        raise Exception("Only admins and moderators can get this operation")
    try:
        users = session.query(UserTable).filter(UserTable.role_id != 3, UserTable.kpd_score > 0).all()
        return users
    except Exception as e:
        raise e


# Отмена всех уведомлений (доступ только у администратора)
def cancel_all_notifications(current_user, session):
    if current_user.role_id != 3:
        raise Exception("Only admins can cancel notifications.")

    try:
        session.query(NotificationTable).update({NotificationTable.is_notificated: True})
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


# Удаление уведомления (доступ только у администратора)
def delete_notification(notification_id, current_user, session):
    if current_user.role_id != 3:
        raise Exception("Only admins can delete notifications.")

    try:
        notification = session.query(NotificationTable).get(notification_id)
        if notification is None:
            raise Exception(f"Notification with ID {notification_id} not found.")

        session.delete(notification)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e


# Изменение уведомления (доступ только у администратора)
def update_notification(notification_id, updated_notification, current_user, session):
    if current_user.role_id != 3:
        raise Exception("Only admins can update notifications.")

    try:
        notification = session.query(NotificationTable).get(notification_id)
        if notification is None:
            raise Exception(f"Notification with ID {notification_id} not found.")

        for key, value in updated_notification.items():
            setattr(notification, key, value)

        session.commit()
        return notification
    except Exception as e:
        session.rollback()
        raise e


# Создание уведомления (доступ только у администратора)
def create_notification(notification_data, current_user, session):
    if current_user.role_id != 3:
        raise Exception("Only admins can create notifications.")

    try:
        new_notification = NotificationTable(**notification_data)
        session.add(new_notification)
        session.commit()
        return new_notification
    except Exception as e:
        session.rollback()
        raise e


# Чтение фидбека (доступ только у администратора)
def read_feedback(feedback_id, current_user, session):
    if current_user.role_id != 3:
        raise Exception("Only admins can read feedback.")

    try:
        feedback = session.query(FeedbackTable).get(feedback_id)
        if feedback is None:
            raise Exception(f"Feedback with ID {feedback_id} not found.")

        return feedback
    except Exception as e:
        raise e


# Создание фидбека (доступ только у пользователя)
def create_feedback(feedback_message, score: FeedbackScore, current_user, session):
    try:
        new_feedback = FeedbackTable()
        new_feedback.message = feedback_message
        new_feedback.feedback_score = score
        new_feedback.user_id = current_user.id
        session.add(new_feedback)
        session.commit()
        return new_feedback
    except Exception as e:
        session.rollback()
        raise e


# Форсированная смена пароля у пользователя (доступ только у администратора)
def force_change_password(full_name, new_password, current_user, session):
    if current_user.role_id != 3:
        raise Exception("Access denied")

    try:
        user = session.query(UserTable).filter(UserTable.full_name == full_name).first()
        if user is None:
            raise Exception("User not found")

        user.password = new_password
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e


# Смена своего пароля после авторизации
def change_password(new_password, current_user, session):
    try:
        user = session.query(UserTable).filter(UserTable.id == current_user.id).first()
        user.password = new_password
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e


# Деаутентификация со всех аккаунтов после авторизации (зануление ID в VK и TG) (доступ только у пользователя)
def deauthenticate(current_user, session) -> bool:
    try:
        current_user.tg_id = None
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e


# Авторизация (привязка ID после ввода пароля)
def authenticate(tg_id, password, session) -> bool:
    try:
        user = session.query(UserTable).filter(UserTable.password == password).first()
        if user is None:
            session.rollback()
            raise Exception("User not found")

        user.tg_id = tg_id
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e


def get_tg_id_all_users(session):
    try:
        users = session.query(UserTable.tg_id).filter(UserTable.role_id != 3).filter(UserTable.tg_id is not None).all()
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
