import telebot
from telebot.types import MessageAutoDeleteTimerChanged
import markups
import sql_app.utils.crud as crud
import sql_app.models.models as models
from sql_app.database.database import SessionLocal, engine
import functions

from dotenv import load_dotenv
import os

load_dotenv()

IS_PRODUCTION_MODE = bool(int(os.environ.get("IS_PRODUCTION_MODE")))

token = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(token)

session_set = set()


# region Main node
@bot.message_handler(func=lambda message: True)
def message_handler(message):
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
    if call.from_user.id in session_set:
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
    elif call.data == "get_other_kpd":
        get_other_kpd(call.from_user.id)
# endregion


# region Chains
# region Get other KPD
def get_other_kpd(tg_id: int) -> None:
    session_set.add(tg_id)
    send = bot.send_message(tg_id, "Напишите номер зачетки студента:")
    bot.register_next_step_handler(send, choose_kpd_from_other)


def choose_kpd_from_other(message):
    if not message.text.isdigit():
        session_set.discard(message.from_user.id)
        bot.send_message(message.from_user.id, "Некорректный ввод")
        return
    session = SessionLocal(bind=engine)
    user_initiator = session.query(models.UserTable).filter(models.UserTable.tg_id == str(message.from_user.id)).first()
    if not user_initiator or user_initiator.role.acsess_level < 2:
        session.close()
        session_set.discard(message.from_user.id)
        return
    user_target = session.query(models.UserTable).filter(models.UserTable.student_id == int(message.text)).first()
    
    if not user_target:
        session.close()
        session_set.discard(message.from_user.id)
        bot.send_message(message.from_user.id, "Студент не найден")
        return
    events = session.query(models.EventLogTable).filter(models.EventLogTable.event_target_id == user_target.id).all()
    answer = functions.event_converter_to_message(events=events)
    session.close()
    send = bot.send_message(message.from_user.id, "Напишите номер конкретного случая: \n" + answer)
    bot.register_next_step_handler(send, get_info_about_concrete_kpd)
    
def get_info_about_concrete_kpd(message) -> None:
    session = SessionLocal(bind=engine)
    pictures = session.query(models.ImageTable).filter(models.ImageTable.event_id == int(message.text)).all()
    event_data = session.query(models.EventLogTable).filter(models.EventLogTable.id == int(message.text)).first()
    for picture in pictures:
        bot.send_photo(message.from_user.id, photo=picture.image_id)
    bot.send_message(message.from_user.id, str(event_data.created_at) + "\n" + event_data.message + "\nНачислено быллов КПД: " + str(event_data.kpd_diff))
    session_set.discard(message.from_user.id)
    session.close()

# endregion


# region Get Profile
def get_other_profile(tg_id: int) -> None:
    
    session_set.add(tg_id)
    send = bot.send_message(tg_id, "Напишите номер блока:")
    bot.register_next_step_handler(send, print_other_profiles)


def print_other_profiles(message):
    answer = ""
    session_set.discard(message.from_user.id)
    if len(message.text) < 4 or not message.text[0:3:].isdigit() or not message.text[3].isalpha():
        bot.send_message(message.from_user.id, "Некорректный ввод")
        return
    session = SessionLocal(bind=engine)
    room = session.query(models.RoomTable).filter(models.RoomTable.number == message.text.strip()).first()
    if not room:
        bot.send_message(message.from_user.id, "Некорректный ввод")
        session.close()
        return
    users = session.query(models.UserTable).filter(models.UserTable.room_id == room.id).all()
    for i in users:
        answer += str(i.student_id) + " | " + i.name + " " + i.sname + "\n"
    session.close()
    bot.send_message(message.from_user.id, answer)
# endregion


# region Set KPD chain
def set_kpd_chain(tg_id: int) -> None:
    send = bot.send_message(tg_id, "Напишите номер студ билета:")
    bot.register_next_step_handler(send, set_kpd_fullname_getter)
    session_set.add(tg_id)


def set_kpd_fullname_getter(message) -> None:
    if not message.text.isdigit():
        send = bot.send_message(message.from_user.id, "Incorrect input")
        session_set.discard(message.from_user.id)
        return
    target_id = None
    if IS_PRODUCTION_MODE:
        session = SessionLocal(bind=engine)
        user = session.query(models.UserTable).filter(models.UserTable.student_id == int(message.text)).first()
        user_initiator = crud.get_user_by_tg_id(message.from_user.id, session)
        event_types = crud.get_all_event_types(session)
        session.close()
        if user:
            target_id = user.id
        else:
            bot.send_message(message.from_user.id, "Студент не найден.")
            session_set.discard(message.from_user.id)
            return
    else:
        user = models.UserTable(full_name="TEST TEST")
        session_set.discard(message.from_user.id)
    
    answer: str = "Выберите тип причины:"
    for i in range(len(event_types)):
        answer += "\n[" + str(i) + "]" + event_types[i].name
    send = bot.send_message(message.from_user.id, answer)
    bot.register_next_step_handler(send, set_kpd_type_getter, e_types=event_types, target_id=target_id)


def set_kpd_type_getter(message, e_types: [models.EventTypeTable] = None, target_id: int = None) -> None:
    if not e_types or not target_id or not message.text.isdigit() or int(message.text) >= len(e_types):
        session_set.discard(message.from_user.id)
        return
    event_type_id = e_types[int(message.text)].id
    send = bot.send_message(message.from_user.id, "Приложите 1 фото")
    bot.register_next_step_handler(send, set_kpd_images, target_id=target_id, e_type=event_type_id)


def set_kpd_images(message, target_id: int = None, e_type: int = None) -> None:
    if not message.photo:
        send = bot.send_message(message.from_user.id, "Приложите именно фото. Возврат...")
        session_set.discard(message.from_user.id)
        return
    photo_ids = [message.photo[-1]]
    send = bot.send_message(message.from_user.id, "Напишите развёрнуто причину")
    bot.register_next_step_handler(send, set_kpd_message_getter, photo_ids=photo_ids, target_id=target_id, e_type=e_type)


def set_kpd_message_getter(message, photo_ids: [str], target_id: int = None, e_type: int = None) -> None:
    if not photo_ids:
        session_set.discard(message.from_user.id)
        return
    send = bot.send_message(message.from_user.id, "Напишите количество баллов")
    bot.register_next_step_handler(send, set_kpd_deff_score_getter, photo_ids=photo_ids, target_id=target_id, e_type=e_type, e_message=message.text)


def set_kpd_deff_score_getter(message, photo_ids: [str], target_id: int = None, e_type: int = None, e_message: str = None) -> None:
    
    session = SessionLocal(bind=engine)
    in_user = session.query(models.UserTable).filter(models.UserTable.tg_id == str(message.from_user.id)).first()
    subj_user = session.query(models.UserTable).filter(models.UserTable.id == target_id).first()
    subj_user.kpd_score += int(message.text)
    event = models.EventLogTable(message=e_message,
                                 kpd_diff=int(message.text),
                                 event_target_id=target_id,
                                 event_initiator_id=in_user.id,
                                 event_type_id=e_type)
    
    session.add(event)
    session.commit()
    for id in photo_ids:
        session.add(models.ImageTable(image_id=id,
                                        event_id=event.id))
    session.commit()
    session.close()
    bot.send_message(message.from_user.id, "Готово!")
    session_set.discard(message.from_user.id)

# endregion


# region feedback chain
def feedback_info(tg_id: int) -> None:
    send = bot.send_message(tg_id, "Напишите отзыв о работе сотрудника(ов) общежития:")
    bot.register_next_step_handler(send, feedback_body_handler)
    session_set.add(tg_id)


def feedback_body_handler(message) -> None:
    send = bot.send_message(message.from_user.id,
                            "Оцените опыт взаимодействия:\n1 - плохо\n2 - нормально\n3 - хорошо")
    bot.register_next_step_handler(send, feedback_score_handler, fb_message=message.text)


def feedback_score_handler(message, fb_message: str = None) -> None:
    score_of_feedback = -1
    if message.text in ["1", "2", "3"]:
        score_of_feedback = int(message.text)

    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(message.from_user.id, session)

    if not user:
        session.close()
        session_set.discard(message.from_user.id)
        return
    try:
        new_feedback = models.FeedbackTable(message=fb_message,
                                            feedback_score=score_of_feedback,
                                            initiator_id=user.id)
        session.add(new_feedback)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    session_set.discard(message.from_user.id)
    session.close()

    bot.send_message(message.from_user.id, "Спасибо за отзыв!")

# endregion


# region change password chain
def old_password_checker(tg_id: int):
    send = bot.send_message(tg_id, "Для смены пароля введите старый пароль:")
    bot.register_next_step_handler(send, change_password_handler)


def change_password_handler(message):
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(message.from_user.id, session)

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
    session.close()


def change_password_final(message):
    if not message.text.isalnum():
        bot.send_message(message.from_user.id,
                         "Пароль должен содержать только английские буквы и цифры.")
        return

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
    send = bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(send, auth_handler, login=message.text)

def auth_handler(message, login=None):
    try:
        session = SessionLocal(bind=engine)
        crud.authenticate(message.from_user.id, login, message.text, session)
        session.close()
    except BaseException:
        bot.send_message(message.chat.id, 'Неправильный пароль. Попробуйте ещё раз или обратитесь к администрации.')
        auth_query(message)
        return
    finally:
        session_set.discard(message.from_user.id)
    bot.send_message(message.chat.id, 'Вы успешно аутентифицировались')
    bot.delete_message(message.chat.id, message.id)
    message_handler(message=message)
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
