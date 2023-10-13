import telebot
from telebot.types import MessageAutoDeleteTimerChanged
import markups
import sql_app.utils.crud as crud
import sql_app.models.models as models
from sql_app.database.database import SessionLocal, engine

from dotenv import load_dotenv
import os

load_dotenv()

IS_PRODUCTION_MODE = bool(int(os.environ.get("IS_PRODUCTION_MODE")))

token = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(token)


sessions_feedback: dict[str, models.FeedbackTable] = {}
sessions_event: dict[str, models.EventLogTable] = {}
session_through: dict[str, models.ThroughTable] = {}
session_notify: dict[str, models.NotificationTable] = {}
session_auth: dict[str, str] = {}

session_messages_to_clean: dict[str, None]

# region Functions
# O(1) avg
def is_free(tg_id: str) -> bool:
    if tg_id not in session_notify and \
       tg_id not in sessions_event and \
       tg_id not in session_through and \
       tg_id not in session_notify and \
       tg_id not in session_auth:
        return True
    return False

def del_hist(message, count=5):
    chat_id = message.chat.id
    message_id = message.message_id
    for i in range(message_id, message_id - count, -1):
        try:
            bot.delete_message(chat_id, i)
        except BaseException:
            pass

# O(n) avg
def sort_file_signatures(photo: [str]) -> [str]:
    set_of_signatures = set()
    ans_list = []
    for i in photo:
        if i.split("-")[0] not in set_of_signatures:
            set_of_signatures.add(i.split("-")[0])
            ans_list.append(i)
    return ans_list
# endregion

# region Main node
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if message.text == "tf":

        session = SessionLocal(bind=engine)
        photos = session.query(models.ImageTable).all()
        for i in photos:
            bot.send_photo(message.chat.id, i.image_id)

        session.close()
        return

    session = SessionLocal(bind=engine)
    user = None
    if IS_PRODUCTION_MODE:
        user = crud.get_user_by_tg_id(message.from_user.id, session)
    else:
        if input("is authed? y/n") == "y":
            user = models.UserTable(role_id=int(input("test role:")), full_name="TESTNAME")
    if user is None:
        auth_query(message)
    elif user.role.acsess_level >= 3:
        bot.send_message(message.chat.id, "Основное меню администратора:",
                         reply_markup=markups.gen_admin())
    elif user.role.acsess_level == 2:
        bot.send_message(message.chat.id, "Основное меню модератора:",
                         reply_markup=markups.gen_moder_main())
    elif user.role.acsess_level <= 1:
        bot.send_message(message.chat.id, "Основное меню:",
                         reply_markup=markups.gen_stud())
    else:
        print("unhandled role ```message_handler```")
    
    session.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if not is_free(call.from_user.id):
        return

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
        get_other_profile(call.from_user.id)
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
# region Get Profile
def get_other_profile(tg_id: int) -> None:
    send = bot.send_message(tg_id, "Напишите номер блока:")
    bot.register_next_step_handler(send, print_other_profiles)


def print_other_profiles(message):
    answer = ""
    if not message.text[0:3:].isdigit() or not message.text[3].isalpha():
        bot.send_message(message.from_user.id, "Некорректный ввод")
        return
    session = SessionLocal(bind=engine)
    room = session.query(models.RoomTable).filter(models.RoomTable.number == message.text.strip())
    if not room:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        session.close()
        return
    users = session.query(models.UserTable).filter

    session.close()
    bot.send_message(message.from_user.id, answer)
# endregion


# region Set KPD chain
def set_kpd_chain(tg_id: int) -> None:
    send = bot.send_message(tg_id, "Напишите номер студ билета:")
    bot.register_next_step_handler(send, set_kpd_fullname_getter)


def set_kpd_fullname_getter(message) -> None:
    if not message.text.isdigit():
        send = bot.send_message(message.from_user.id, "Incorrect input")
        return
    if IS_PRODUCTION_MODE:
        session = SessionLocal(bind=engine)
        user = session.query(models.UserTable).filter(models.UserTable.student_id == int(message.text))
        user_initiator = crud.get_user_by_tg_id(message.from_user.id, session)
        event_types = crud.get_all_event_types(session)
        session.close()
        if user:
            sessions_event.update({str(message.from_user.id): models.EventLogTable(event_target_id=user.id,
                                                                                   event_initiator_id=user_initiator.id)})
        else:
            if str(message.from_user.id) in sessions_event:
                sessions_event.pop(str(message.from_user.id))
            bot.send_message(message.from_user.id, "Студент не найден.")
            return
    else:
        user = models.UserTable(full_name="TEST TEST")
    
    answer: str = "Выберите тип причины:"
    for i in range(len(event_types)):
        answer += "\n[" + str(i) + "]" + event_types[i].name
    send = bot.send_message(message.from_user.id, answer)
    bot.register_next_step_handler(send, set_kpd_type_getter, e_types=event_types)


def set_kpd_type_getter(message, e_types: [models.EventTypeTable] = None) -> None:
    event: models.EventLogTable = None
    try:
        event = sessions_event.get(str(message.from_user.id))
        int(message.text)
    except BaseException:
        if str(message.from_user.id) in sessions_event:
            sessions_event.pop(str(message.from_user.id))
        return

    if event:
        event.event_type_id = e_types[int(message.text)].id
        sessions_event.update({str(message.from_user.id): event})
        send = bot.send_message(message.from_user.id, "Приложите фото")
        bot.register_next_step_handler(send, set_kpd_images)
    else:
        return


def set_kpd_images(message) -> None:
    if not message.photo:
        send = bot.send_message(message.from_user.id, "Приложите фото")
        bot.register_next_step_handler(send, set_kpd_images)
        if str(message.from_user.id) in sessions_event:
            sessions_event.pop(str(message.from_user.id))
        return
    
    photo_ids = sort_file_signatures([photo.file_id for photo in message.photo])

    send = bot.send_message(message.from_user.id, "Напишите развёрнуто причину")
    bot.register_next_step_handler(send, set_kpd_message_getter, photo_ids=photo_ids)


def set_kpd_message_getter(message, photo_ids: [str]) -> None:
    event: models.EventLogTable = None
    try:
        event = sessions_event.get(str(message.from_user.id))
    except BaseException:
        if str(message.from_user.id) in sessions_event:
            sessions_event.pop(str(message.from_user.id))
        return
    
    if event:
        event.message = message.text
        sessions_event.update({str(message.from_user.id): event})
        send = bot.send_message(message.from_user.id, "Напишите количество баллов")
        bot.register_next_step_handler(send, set_kpd_deff_score_getter, photo_ids=photo_ids)
    else:
        return


def set_kpd_deff_score_getter(message, photo_ids: [str]) -> None:
    event: models.EventLogTable = None
    try:
        event = sessions_event.get(str(message.from_user.id))
    except BaseException:
        if str(message.from_user.id) in sessions_event:
            sessions_event.pop(str(message.from_user.id))
        return
    
    if event:
        session = SessionLocal(bind=engine)
        subj_user = session.query(models.UserTable).filter(models.UserTable.id == event.event_target_id).first()
        subj_user.kpd_score += int(message.text)
        event.kpd_diff = int(message.text)
        session.add(event)
        session.commit()
        for id in photo_ids:
            session.add(models.ImageTable(image_id=id,
                                          event_id=event.id))
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
                            "Оцените опыт взаимодействия:\n1 - плохо\n2 - нормально\n3 - хорошо")
    bot.register_next_step_handler(send, feedback_score_handler)


def feedback_score_handler(message) -> None:
    score_of_feedback = 2
    if message.text in ["1", "2", "3"]:
        score_of_feedback = int(message.text)

    if IS_PRODUCTION_MODE:
        session = SessionLocal(bind=engine)
        user = crud.get_user_by_tg_id(message.from_user.id, session)

        if not user:
            print("user not found")
            session.close()
            if str(message.from_user.id) in sessions_feedback:
                sessions_feedback.pop(str(message.from_user.id))
            return
        try:
            new_feedback = sessions_feedback.get(str(message.from_user.id))
            if new_feedback:
                new_feedback.initiator_id = user.id
                new_feedback.feedback_score = score_of_feedback
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
        user = crud.get_user_by_tg_id(message.from_user.id, session)
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
        user = crud.get_user_by_tg_id(message.from_user.id, session)
        try:
            crud.change_password(new_pwd, user, session)
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.from_user.id,
                            "Пароль успешно изменён.")
        except BaseException:
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.from_user.id,
                                "Возникли проблемы смены пароля.")
        finally:
            session.close()

# endregion


# region Auth chain
def auth_query(message):
    send = bot.send_message(message.chat.id, 'Введите логин:')
    bot.register_next_step_handler(send, auth_pwd)


def auth_pwd(message):
    session_auth.update({str(message.from_user.id): message.text})
    send = bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(send, auth_handler)

def auth_handler(message):
    if IS_PRODUCTION_MODE:
        try:
            session = SessionLocal(bind=engine)
            crud.authenticate(message.from_user.id, session_auth[str(message.from_user.id)], message.text, session)
            session.close()
        except BaseException:
            bot.send_message(message.chat.id, 'Неправильный пароль. Попробуйте ещё раз или обратитесь к администрации.')
            auth_query(message)
            return
        finally:
            if str(message.from_user.id) in session_auth:
                session_auth.pop(str(message.from_user.id))
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
    user = crud.get_user_by_tg_id(tg_id, session)
    if not user:
        session.close()
        return
    
    events = crud.get_event_by_event_target_id(user, 5, session)
    session.close()

    ans = "\n".join(["Дата: " + str(i.created_at) + "\nПричина: " + str(i.message) + "\nКол-во баллов: " +
                     str(i.kpd_diff) + "\n----------" for i in events]) if events else "У вас нет КПД"
    bot.send_message(tg_id, "История КПД\n----------\n" + ans)


# profile OUTPUT METHOD
def profile_output(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(tg_id, session)
    ans = "Профиль\nВаше имя - " + user.name + " " + user.sname + \
          "\nРоль " + user.role.name + "\nБаллы КПД - " + str(user.kpd_score)
    session.close()
    bot.send_message(tg_id, ans)


# LIST NOTIFICATION OUTPUT METHOD
def list_notifications_output(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(tg_id, session)
    ans = crud.get_all_not_notified(user, session=session)
    session.close()
    bot.send_message(tg_id, ans)


# cancel ALL NOTIFICATIONS OUTPUT METHOD
def cancel_all_notifications(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(str(tg_id), session)
    crud.cancel_all_notifications(user, session=session)
    session.close()


# GET LIST POSITIVE KPD
def get_list_kpd(tg_id: int) -> None:
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(tg_id, session)
    if not user:
        session.close()
        return
    users = crud.get_users_with_positive_kpd(user, session)
    session.close()
    if not users:
        return 
    ans = "positive KPD:\n"
    for i in users:
        ans += str(i.student_id) + i.name + " " + i.sname + " " + str(i.kpd_score) + "\n"
    bot.send_message(tg_id, ans)


# endregion


bot.infinity_polling()
