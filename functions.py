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