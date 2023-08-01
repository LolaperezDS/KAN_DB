import telebot
import time
from datetime import timedelta, datetime
import sql_app.utils.crud as crud
import sql_app.models.models as models

from sql_app.database.database import SessionLocal, engine

# in secs, between checks
FREEZE_TIME = 10


async def async_notificate_all_users(users: [str], message: str, bot_implementer: telebot.TeleBot) -> None:
    notificate_all_users(users, message, bot_implementer)
    return


def notificate_all_users(users: [str], message: str, bot_implementer: telebot.TeleBot):
    for user in users:
        try:
            bot_implementer.send_message(int(user), message)
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось напомнить пользователю " + str(user))


def message_to_notificate_constructor(notification: models.NotificationTable) -> str:
    return "До события часов: " + str(notification.remind_hours) + "\nСуть события: " + notification.message


if __name__ == "__main__":
    token = "6012918807:AAGmDv1adk0ic1RtlUuDgCbdCnS0QoYP9Dc"
    bot = telebot.TeleBot(token)

    session = SessionLocal(bind=engine)
    tg_users_to_notificate = crud.get_tg_id_all_users(session)
    session.close()
    while True:
        session = SessionLocal(bind=engine)
        notifications = crud.get_all_not_notified(session)
        session.close()
        # проверить все напоминания
        for notification in notifications:
            if notification.event_date - timedelta(hours=notification.remind_hours) >= datetime.utcnow():
                notificate_all_users(tg_users_to_notificate, message_to_notificate_constructor(notification), bot)
                crud.cancel_notification_by_id(notification.id, session)
                continue

        time.sleep(FREEZE_TIME)
