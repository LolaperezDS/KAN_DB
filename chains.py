import telebot
import markups
import sql_app.utils.crud as crud
import sql_app.models.models as models
from sql_app.database.database import SessionLocal, engine

from dotenv import load_dotenv
import os

load_dotenv()

IS_PRODUCTION_MODE = bool(int(os.environ.get("IS_PRODUCTION_MODE")))

token = "6012918807:AAGmDv1adk0ic1RtlUuDgCbdCnS0QoYP9Dc"
bot = telebot.TeleBot(token)


sessions_feedback: dict[str, models.FeedbackTable] = {}
sessions_event: dict[str, models.EventLogTable] = {}


# region Main node
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if IS_PRODUCTION_MODE:
        session = SessionLocal(bind=engine)
        user = crud.get_user_by_tg_id(str(message.from_user.id), session)
        session.close()
    else:
        if input("is authed? y/n") == "y":
            user = models.UserTable(role_id=int(input("test role:")), full_name="TESTNAME")
        else:
            user = None
    if user is None:
        auth_query(message)
    elif user.role_id == 1:
        bot.send_message(message.chat.id, "Основное меню администратора:",
                         reply_markup=markups.gen_admin())
    elif user.role_id == 2:
        bot.send_message(message.chat.id, "Основное меню модератора:",
                         reply_markup=markups.gen_moder_main())
    elif user.role_id == 3:
        bot.send_message(message.chat.id, "Основное меню:",
                         reply_markup=markups.gen_stud())
    else:
        print("unhandled role ```message_handler```")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "profile":
        profile_output(call.from_user.id)
    elif call.data == "kpd":
        kpd_handler(call.from_user.id)
    elif call.data == "info":
        info_output(call.from_user.id)
    elif call.data == "ch_pwd":
        old_password_checker(call.from_user.id)
    elif call.data == "feedback":
        feedback_info(call.from_user.id)
    elif call.data == "moder_panel":
        bot.send_message(call.from_user.id, "Панель модератора:",
                         reply_markup=markups.gen_moder_panel())
    elif call.data == "set_kpd":
        set_kpd_chain(call.from_user.id)
    elif call.data == "return_m":
        bot.send_message(call.from_user.id, "Основное меню модератора:",
                         reply_markup=markups.gen_moder_main())
    elif call.data == "get_other_profile":
        raise NotImplementedError
    elif call.data == "get_list_kpd":
        get_list_kpd(call.from_user.id)
    elif call.data == "notification_menu":
        bot.send_message(call.from_user.id, "Панель редактирования событий:",
                         reply_markup=markups.gen_notification())
    elif call.data == "create_notification":
        raise NotImplementedError
    elif call.data == "list_notifications":
        list_notifications_output(call.from_user.id)
    elif call.data == "delete_notification":
        raise NotImplementedError
    elif call.data == "cancel_all_notifications":
        cancel_all_notifications(call.from_user.id)
    elif call.data == "return_a":
        bot.send_message(call.from_user.id, "Основное меню администратора:",
                         reply_markup=markups.gen_admin())
# endregion


# region Chains
# region Set KPD chain
def set_kpd_chain(tg_id: int) -> None:
    send = bot.send_message(tg_id, "Напишите Фио студента:")
    bot.register_next_step_handler(send, set_kpd_fullname_getter)


def set_kpd_fullname_getter(message) -> None:
    if IS_PRODUCTION_MODE:
        session = SessionLocal(bind=engine)
        user = crud.get_user_by_full_name(message.text, session)
        user_initiator = crud.get_user_by_tg_id(str(message.from_user.id), session)
        session.close()
        if user:
            sessions_event.update({str(message.from_user.id): models.EventLogTable(event_target_id=user.id,
                                                                                   event_initiator_id=user_initiator.id)})
    else:
        user = models.UserTable(full_name="TEST TEST")

    if not user:
        bot.send_message(message.from_user.id, "Студент с таким фио не найден.")
        return
    send = bot.send_message(message.from_user.id, "Напишите кратко суть изменения баллов КПД")
    bot.register_next_step_handler(send, set_kpd_type_getter)


def set_kpd_type_getter(message) -> None:
    event = sessions_event.get(str(message.from_user.id))
    if event:
        event.event_type = message.text
        sessions_event.update({str(message.from_user.id): event})
        send = bot.send_message(message.from_user.id, "Напишите развёрнуто причину")
        bot.register_next_step_handler(send, set_kpd_message_getter)
    else:
        return


def set_kpd_message_getter(message) -> None:
    event = sessions_event.get(str(message.from_user.id))
    if event:
        event.message = message.text
        sessions_event.update({str(message.from_user.id): event})
        send = bot.send_message(message.from_user.id, "Напишите количество баллов")
        bot.register_next_step_handler(send, set_kpd_deff_score_getter)
    else:
        return


def set_kpd_deff_score_getter(message) -> None:
    event = sessions_event.get(str(message.from_user.id))

    session = SessionLocal(bind=engine)
    subj_user = session.query(models.UserTable).filter(models.UserTable.id == event.event_target_id).first()
    setattr(subj_user, "kpd_score", subj_user.kpd_score + int(message.text))

    session.commit()
    session.close()

    if event:
        event.kpd_diff = int(message.text)
        session = SessionLocal(bind=engine)
        session.add(event)
        session.commit()
        session.close()
        sessions_event.pop(str(message.from_user.id))
    bot.send_message(message.from_user.id, "Готово!")

# endregion


# region feedback chain
def feedback_info(tg_id: int) -> None:
    send = bot.send_message(tg_id, "Напишите отзыв о работе сотрудника(ов) общежития:")
    bot.register_next_step_handler(send, feedback_body_handler)


def feedback_body_handler(message) -> None:
    if IS_PRODUCTION_MODE:
        sessions_feedback.update({str(message.from_user.id): models.FeedbackTable(message=message.text)})
    else:
        print("Feedback from: " + str(message.from_user.id) + " = " + message.text)
    send = bot.send_message(message.from_user.id,
                            "Оцените экспириенс взаимодействия:\n1 - плохо\n2 - нормально\n3 - хорошо")
    bot.register_next_step_handler(send, feedback_score_handler)


def feedback_score_handler(message) -> None:
    score_of_feedback = 2
    if message.text in ["1", "2", "3"]:
        score_of_feedback = int(message.text)

    if IS_PRODUCTION_MODE:
        session = SessionLocal(bind=engine)
        user = crud.get_user_by_tg_id(str(message.from_user.id), session)

        if not user:
            print("user not found")
            session.close()
            return
        try:
            new_feedback = sessions_feedback.get(str(message.from_user.id))
            if new_feedback:
                new_feedback.user_id = user.id
                new_feedback.feedback_score = models.FeedbackScore(score_of_feedback)
                session.add(new_feedback)
                session.commit()
                sessions_feedback.pop(str(message.from_user.id))
        except Exception as e:
            session.rollback()
            raise e
        session.close()
    else:
        print("Фидбек как будто бы создан")

    bot.send_message(message.from_user.id, "Спасибо за отзыв!")

# endregion


# region change password chain
def old_password_checker(tg_id: int):
    send = bot.send_message(tg_id, "Для смены пароля введите старый пароль:")
    bot.register_next_step_handler(send, change_password_handler)


def change_password_handler(message):
    if IS_PRODUCTION_MODE:
        session = SessionLocal(bind=engine)
        user = crud.get_user_by_tg_id(str(message.from_user.id), session)
        session.close()

        old_pwd = message.text

        if not old_pwd.isalnum():
            bot.reply_to(message, "Не удалось сменить пароль. Вы ввели некорректный старый пароль.")
            return

        if old_pwd == user.password:
            bot.delete_message(message.chat.id, message.id)
            send = bot.send_message(message.from_user.id,
                                    "Введите новый пароль (он должен содержать только английские буквы и цифры):")
            bot.register_next_step_handler(send, change_password_final)
        else:
            bot.reply_to(message, "Не удалось сменить пароль. Вы ввели некорректный старый пароль.")
    else:
        print("Как будто пользователь ввёл правильный старый пароль: " + message.text)


def change_password_final(message):
    if not IS_PRODUCTION_MODE:
        print("Как будто пользователь ввёл новый пароль: " + message.text)

    if not message.text.isalnum():
        bot.send_message(message.from_user.id,
                         "Пароль должен содержать только английские буквы и цифры.")
        return

    if IS_PRODUCTION_MODE:
        new_pwd = message.text
        session = SessionLocal(bind=engine)
        user = crud.get_user_by_tg_id(str(message.from_user.id), session)
        crud.change_password(new_pwd, user, session)
        session.close()

    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.from_user.id,
                     "Пароль успешно изменён.")
# endregion


# region Auth chain
def auth_query(message):
    send = bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(send, auth_handler)


def auth_handler(message):
    if IS_PRODUCTION_MODE:
        try:
            session = SessionLocal(bind=engine)
            crud.authenticate(str(message.from_user.id), message.text, session)
            session.close()
        except BaseException:
            bot.send_message(message.chat.id, 'Неправильный пароль. Попробуйте ещё раз или обратитесь к администрации.')
            auth_query(message)
            return
        bot.send_message(message.chat.id, 'Вы успешно аутентифицировались')
        bot.delete_message(message.chat.id, message.id)
        message_handler(message=message)
    else:
        print("Как будто пользователь попытался аутентифицироваться: " + message.text)
# endregion
# endregion


# region Single methods
# INFO METHOD
def info_output(tg_id: int) -> None:
    raise NotImplementedError


# KPD OUTPUT METHOD
def kpd_handler(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    profile = crud.get_own_profile_by_tg_id(str(tg_id), session)
    events = crud.get_event_by_event_target_id(profile.get("id"), 5, session)
    session.close()

    ans = "\n".join(["Дата: " + str(i.created_at) + "\nПричина: " + str(i.message) + "\nКол-во баллов: " +
                     str(i.kpd_diff) + "\n----------" for i in events]) if events else "У вас нет КПД"

    bot.send_message(tg_id, "История КПД\n----------\n" + ans)


# profile OUTPUT METHOD
def profile_output(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    profile = crud.get_own_profile_by_tg_id(str(tg_id), session)
    session.close()
    ans = "Профиль\nВаше имя - " + profile.get("full_name") + \
          "\nРоль " + profile.get("role") + "\nБаллы КПД - " + str(profile.get("kpd_score"))
    bot.send_message(tg_id, ans)


# LIST NOTIFICATION OUTPUT METHOD
def list_notifications_output(tg_id: int) -> None:
    raise NotImplementedError


# cancel ALL NOTIFICATIONS OUTPUT METHOD
def cancel_all_notifications(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(str(tg_id), session)
    crud.cancel_all_notifications(user, session=session)
    session.close()


# GET LIST POSITIVE KPD
def get_list_kpd(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(str(tg_id), session)

    users = crud.get_users_with_positive_kpd(user, session)
    ans = "positive KPD:\n"
    for i in users:
        ans += i.full_name + " " + str(i.kpd_score) + "\n"
    bot.send_message(tg_id, ans)

    session.close()

# endregion


bot.infinity_polling()
