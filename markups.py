import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv


def gen_stud() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Профиль", callback_data="profile"),
               InlineKeyboardButton("КПД", callback_data="kpd"),
               InlineKeyboardButton("Информация", callback_data="info"),
               InlineKeyboardButton("Изменить пароль", callback_data="ch_pwd"),
               InlineKeyboardButton("Отзыв", callback_data="feedback"))
    return markup


def gen_moder_main() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Профиль", callback_data="profile"),
               InlineKeyboardButton("КПД", callback_data="kpd"),
               InlineKeyboardButton("Информация", callback_data="info"),
               InlineKeyboardButton("Изменить пароль", callback_data="ch_pwd"),
               InlineKeyboardButton("Модераторская панель", callback_data="moder_panel"))
    return markup


def gen_moder_panel() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Поставить КПД", callback_data="set_kpd"),
               InlineKeyboardButton("Предыдущее меню", callback_data="return_m"),
               InlineKeyboardButton("Профиль человека", callback_data="get_other_profile"),
               InlineKeyboardButton("Список КПД>0", callback_data="get_list_kpd"))
    return markup


def gen_admin() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Поставить КПД", callback_data="set_kpd"),
               InlineKeyboardButton("Ивент меню", callback_data="notification_menu"),
               InlineKeyboardButton("Профиль человека", callback_data="get_other_profile"),
               InlineKeyboardButton("Список КПД>0", callback_data="get_list_kpd"))
    return markup


def gen_notification() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Создать напоминание", callback_data="create_notification"),
               InlineKeyboardButton("Список напоминаний", callback_data="list_notifications"),
               InlineKeyboardButton("Удалить напоминание", callback_data="delete_notification"),
               InlineKeyboardButton("Отменить все напоминания", callback_data="cancel_all_notifications"),
               InlineKeyboardButton("Предыдущее меню", callback_data="return_a"))
    return markup


if __name__ == "__main__":
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    bot = telebot.TeleBot(token)

    @bot.message_handler(func=lambda message: True)
    def message_handler(message):
        bot.send_message(message.chat.id, "Желаемое действие:", reply_markup=gen_stud())
        bot.send_message(message.chat.id, "Желаемое действие:", reply_markup=gen_moder_main())
        bot.send_message(message.chat.id, "Желаемое действие:", reply_markup=gen_moder_panel())
        bot.send_message(message.chat.id, "Желаемое действие:", reply_markup=gen_admin())
        bot.send_message(message.chat.id, "Желаемое действие:", reply_markup=gen_notification())


    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "profile":
            pass
        elif call.data == "kpd":
            pass
        elif call.data == "info":
            pass
        elif call.data == "ch_pwd":
            pass
        elif call.data == "feedback":
            pass

    bot.infinity_polling()
