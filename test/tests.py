from sql_app.models.models import UserTable, FeedbackScore

from sql_app.utils.crud import create_user, update_user, delete_user, get_all_users, get_own_profile_by_vk_id, \
    get_own_profile_by_tg_id, create_event, get_event_by_id, get_event_by_event_target_id, \
    get_users_with_positive_kpd, cancel_all_notifications, delete_notification, update_notification, \
    create_notification, read_feedback, \
    create_feedback, force_change_password, change_password, deauthenticate, authenticate

from sql_app.database.database import SessionLocal, engine

from datetime import datetime, timedelta

# Создаем сессию с привязкой к движку
session = SessionLocal(bind=engine)

current_user = UserTable(id=1,
                         is_active=True,
                         vk_id="horoshi_chelik",
                         tg_id="mamochka_v_dekrete",
                         password="1",
                         full_name="samat",
                         kpd_score=100,
                         role_id=1)

common_user = UserTable(id=3,
                        is_active=True,
                        vk_id="2",
                        tg_id="2",
                        password="2",
                        full_name="2",
                        kpd_score=2,
                        role_id=3)

user_data = {
    'is_active': True,
    'vk_id': None,
    'tg_id': None,
    'password': '123',
    'full_name': 'amir',
    'kpd_score': 100,
    'role_id': 2
}

updated_user = {
    'is_active': False,
    'full_name': 'John Doe',
    'kpd_score': 100
}

event_data = {
    'event_type': 'New Event1',
    'message': 'A new event has been created1.',
    'kpd_diff': 120,
}

updated_notification = {
    'event_date': datetime.utcnow() + timedelta(hours=2),
    'remind_hours': 1,
    'message': 'Updated notification message',
    'is_notificated': True
}

notification_data = {
    "event_date": datetime.utcnow(),
    "remind_hours": 24,
    "message": "Reminder: Don't forget the meeting tomorrow!",
    "is_notificated": False,
    "initiator_id": current_user.id
}

feedback_data = {
    'message': 'This is a feedback message.',
    'feedback_score': FeedbackScore.cool
}

if __name__ == "__main__":
    # 1
    try:
        new_user = create_user(user_data=user_data, current_user=current_user, session=session)
        print(f"User {new_user} created successfully.")
    except Exception as e:
        print(f"Failed to create user: {str(e)}")
    finally:
        session.close()

    # 2
    try:
        updated_user = update_user(user_id=2, updated_user=updated_user, current_user=current_user, session=session)
        print(f"User with ID {updated_user.id} has been updated successfully.")
    except Exception as e:
        print(f"Failed to update user: {str(e)}")
    finally:
        session.close()

    # 3
    try:
        deleted = delete_user(user_id=3, current_user=current_user, session=session)
        if deleted:
            print("User deleted successfully.")
        else:
            print("User deletion failed.")
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
    finally:
        session.close()

    # 4
    try:
        users = get_all_users(current_user=current_user, session=session)
        for user in users:
            print(user.full_name)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # 5
    try:
        # vk_id = "12345"  # Ваш VK ID

        profile = get_own_profile_by_vk_id(vk_id="12345", session=session)
        print(profile)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        session.close()

    # 6
    try:
        # tg_id = "1"  # Ваш TG ID

        profile = get_own_profile_by_tg_id(tg_id="1", session=session)
        print(profile)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        session.close()
    #
    # 7
    try:
        new_event = create_event(event_data=event_data, current_user=current_user, session=session)
        print("Event created:", new_event.id, new_event.event_type)
    except Exception as e:
        session.rollback()
        print("Error:", str(e))
    finally:
        session.close()

    # 8
    try:
        # event_id = 2

        event = get_event_by_id(event_id=2, current_user=current_user, session=session)
        print(event.event_type, event.message)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        session.close()

    # 9
    try:
        # event_target_id = 1
        events = get_event_by_event_target_id(event_target_id=3, current_user=current_user, session=session)
        for event in events:
            print(
                f"Event ID: {event.id}, "
                f"Type: {event.event_type}, "
                f"Created At: {event.created_at},"
                f"Message: {event.message}, "
                f"KPD Diff: {event.kpd_diff}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # 10
    try:
        users = get_users_with_positive_kpd(current_user=current_user, session=session)
        for user in users:
            print(f"User ID: {user.id}, Full Name: {user.full_name}, KPD Score: {user.kpd_score}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        session.close()

    # 11
    try:
        cancel_all_notifications(current_user=current_user, session=session)
        print("Notifications cancelled successfully.")
    except Exception as e:
        print("Error cancelling notifications:", str(e))
    finally:
        session.close()

    # 12
    try:
        # notification_id = 1
        delete_notification(notification_id=1, current_user=current_user, session=session)
        print("Notification deleted successfully.")
    except Exception as e:
        print("Failed to delete notification:", str(e))
    finally:
        session.close()

    # 13
    try:
        updated_notification = update_notification(notification_id=3,
                                                   updated_notification=updated_notification,
                                                   current_user=current_user,
                                                   session=session)
        print(f"Notification updated")
    except Exception as e:
        print("Failed to update notification:", str(e))
    finally:
        session.close()

    14
    try:
        new_notification = create_notification(notification_data=notification_data,
                                               current_user=current_user,
                                               session=session)
        print("Notification created:", new_notification.id)
    except Exception as e:
        print("Error creating notification:", str(e))
    finally:
        session.close()

    # 15
    try:
        feedback = read_feedback(feedback_id=1, current_user=current_user, session=session)
        print(feedback.message)
    except Exception as e:
        print(str(e))
    finally:
        session.close()

    # 16
    try:
        new_feedback = create_feedback(feedback_data=feedback_data, current_user=common_user, session=session)
        print(f"Feedback created with ID: {new_feedback.id}")
    except Exception as e:
        print(f"Failed to create feedback: {str(e)}")
    finally:
        session.close()

    # 17
    try:
        # new_password = "popa"
        force_change_password(user_id=3, new_password="popa", current_user=current_user, session=session)
        print("Password changed successfully!")
    except Exception as e:
        print("Error:", str(e))
    finally:
        session.close()

    # 18
    try:
        change_password(new_password="pisya", user_id=1, session=session)
        print("Password changed successfully.")
    except Exception as e:
        print(f"Failed to change password: {str(e)}")
    finally:
        session.close()

    # 19
    try:
        deauthenticate(current_user=common_user, session=session)
        print("User deauthenticated successfully")
    except Exception as e:
        print("Error occurred:", str(e))
    finally:
        session.close()

    # 20
    try:
        authenticated = authenticate(vk_id="2",
                                     tg_id="2",
                                     password="popa",
                                     current_user=common_user,
                                     session=session)
        if authenticated:
            print("Authentication successful")
        else:
            print("Authentication failed")
    except Exception as e:
        print("Authentication error:", str(e))
