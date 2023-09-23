import telebot


token = ""
bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    message_count = 100  # Например, получим последние 100 сообщений

# Получаем историю сообщений
    messages = bot.get_messages(message.chat_id, limit=message_count)

# Выводим сообщения
    for message in messages:
        print(f"{message.date} - {message.from_user.username}: {message.text}")

"""
@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.text)
    pass


# процесс авторизации
# привязка тг айди к профилю в бд
@bot.message_handler(commands=['auth'])
def auth_message(message):
    session = SessionLocal(bind=engine)
    pwd = message.text.split()[-1]
    crud.authenticate(None, str(message.from_user.id), pwd, session)
    session.close()


@bot.message_handler(commands=['help'])
def help_message(message):
    # подробное описание авторизации [если юзер не авторизован]
    # описание команд [в зависимости от привелегии юзера]
    pass


#----------------------------------- [Ю]
# вывод последних 5 ивентов на этот профиль
@bot.message_handler(commands=['KPD'])
def kpd_message(message):
    session = SessionLocal(bind=engine)
    profile = crud.get_own_profile_by_tg_id(str(message.from_user.id), session)
    events = crud.get_event_by_event_target_id(profile.get("id"), 2, session)
    session.close()

    ans = "\n".join([str(i.created_at) + "\t" + str(i.message) + "\t" + str(i.kpd_diff) for i in events]) if events else "У вас нет КПД"

    bot.reply_to(message, "Что то про кпд\n" + ans)

@bot.message_handler(commands=['profile'])
def profile_message(message):
    session = SessionLocal(bind=engine)
    profile = crud.get_own_profile_by_tg_id(str(message.from_user.id), session)
    session.close()
    ans = profile.get("full_name") + ", вы " + profile.get("role") + ". У вас " + str(profile.get("kpd_score")) + " баллов КПД"

    bot.reply_to(message, ans)


@bot.message_handler(commands=['feedback'])
def feedback_message(message):
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(str(message.from_user.id), session)

    if not user:
        print("user not found")
        session.close()
        return
    # TO DO: прикрутить возможность выбирать тип фидбека
    crud.create_feedback(" ".join(message.text.split()[1::]), FeedbackScore.cool, user, session)
    session.close()


@bot.message_handler(commands=['info'])
def info_message(message):
    # вывод инфы об общаге
    pass


@bot.message_handler(commands=['deauth'])
def deauth_message(message):
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(str(message.from_user.id), session)
    if not user:
        print("user not found")
        session.close()
        return
    if crud.deauthenticate(user, session):
        bot.reply_to(message, "Вы успешно отвязали свои аккаунты от приложения")
    session.close()


@bot.message_handler(commands=['change_pwd'])
def change_pwd_message(message):
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(str(message.from_user.id), session)
    if len(message.text.split()) != 3:
        return
    old_pwd = message.text.split()[1]
    new_pwd = message.text.split()[2]
    if old_pwd == user.password:
        crud.change_password(new_pwd, user, session)
        bot.send_message(message.chat.id, "Вы успешно сменили пароль")
        bot.delete_message(message.chat.id, message.id)
    else:
        bot.reply_to(message, "Не удалось сменить пароль")
    session.close()

#-----------------------------------


#----------------------------------- [M]
@bot.message_handler(commands=['all_kpd'])
def all_kpd_message(message):
    # Получение списка всех пользователей с баллами кпд > 0 и они не являются админами
    session = SessionLocal(bind=engine)
    user = crud.get_user_by_tg_id(str(message.from_user.id), session)

    users = crud.get_users_with_positive_kpd(user, session)
    ans = "positive KPD:\n"
    for i in users:
        ans += i.full_name + " " + str(i.kpd_score) + "\n"
    bot.send_message(message.chat.id, ans)

    session.close()


@bot.message_handler(commands=['create_event'])
def create_event_message(message):
    # NOT WORKS
    event_data = {
        'event_type': message.text.split()[4],
        'message': " ".join(message.text.split()[6::]),
        'kpd_diff': int(message.text.split()[5]),
    }
    nameof_subject = " ".join(message.text.split()[1:4:])

    session = SessionLocal(bind=engine)
    profile = crud.get_user_by_tg_id(str(message.from_user.id), session)
    profile_subject = crud.get_user_by_full_name(nameof_subject, session)
    crud.create_event(event_data, profile_subject, profile, session)

    bot.reply_to(message, "Создано")
    session.close()

@bot.message_handler(commands=['get_profile'])
def get_profile_message(message):
    # Чтение юзера
    session = SessionLocal(bind=engine)
    profile = crud.get_user_by_full_name(" ".join(message.text.split()[1::]), session)

    if not profile:
        bot.reply_to(message, "Пользователь с таким именем не найден")
        print(" ".join(message.text.split()[1::]))
        session.close()
        return

    ans = profile.full_name + ", " + str(profile.role.privilege) + ". У юзера " + str(
        profile.kpd_score) + " баллов КПД"

    session.close()
    bot.reply_to(message, ans)

#-----------------------------------


#----------------------------------- [А]
@bot.message_handler(commands=['force_pwd'])
def force_pwd_message(message):
    # форсированная смена пароля у пользователя
    session = SessionLocal(bind=engine)

    new_pwd = message.text.split()[1]
    full_name_to_change = " ".join(message.text.split()[2::])

    profile = crud.get_user_by_tg_id(str(message.from_user.id), session)

    crud.force_change_password(full_name_to_change, new_pwd, profile, session)

    bot.send_message(message.chat.id, "Вы успешно сменили пароль у пользователя " + full_name_to_change)
    bot.delete_message(message.chat.id, message.id)

    session.close()


@bot.message_handler(commands=['create_notification'])
def create_notification_message(message):
    # Добавление напоминания
    pass


@bot.message_handler(commands=['delete_notification'])
def delete_notification_message(message):
    # Удаление напоминания
    pass


@bot.message_handler(commands=['change_notification'])
def change_notification_message(message):
    # Изменение напоминания
    pass


@bot.message_handler(commands=['drop_notification'])
def drop_notification_message(message):
    # Метод, который отменяет все текущие напоминания, то есть изменяет значения в колонне is_notificated на true
    pass


@bot.message_handler(commands=['create_user'])
def create_user_message(message):
    # Создание нового юзера
    pass


@bot.message_handler(commands=['change_user'])
def change_user_message(message):
    # Изменение юзера
    pass


@bot.message_handler(commands=['delete_user'])
def delete_user_message(message):
    # Удаление юзера
    pass
#-----------------------------------

"""
bot.infinity_polling()
