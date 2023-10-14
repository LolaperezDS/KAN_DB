from sql_app.models.models import *


def str_format_to_len(l: int, s: str):
    if len(s) > l:
        return s[:l:]
    return s + " " * (len(s) - l)


def event_converter_to_message(events: [EventLogTable]) -> [str]:
    result = ""
    if not events:
        return "Нет событий"
    for i in events:
        result += str(i.id) + "|" + str_format_to_len(10, i.message) + "|" + str(i.kpd_diff) + "\n"
    return result
