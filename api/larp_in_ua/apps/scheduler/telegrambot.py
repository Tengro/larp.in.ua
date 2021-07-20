from larp_in_ua.apps.scheduler.utils import prepare_events_all, prepare_events_left, prepare_lections_all, prepare_lections_left
from larp_in_ua.apps.common.utils.safe_send import safe_message_send
from django_telegrambot.apps import DjangoTelegramBot
from telegram.ext import CommandHandler


def lections_left(update, context):
    safe_message_send(context.bot, update.message.chat_id, text=prepare_lections_left())


def all_events_left(update, context):
    rows = prepare_events_left()
    if rows:
        for item in row:
            safe_message_send(context.bot, update.message.chat_id, text=item)
    else:
        safe_message_send(context.bot, update.message.chat_id, text="Здається, потік \"Діло\" добігає кінця!")


def all_schedule(update, context):
    lections = prepare_lections_all()
    rows = prepare_events_all()
    if not rows:
        rows = ["Здається, потік \"Діло\" добігає кінця!", ]
    data = [lections, ] + rows
    for data_point in data:
        safe_message_send(context.bot, update.message.chat_id, text=data_point)


def main():
    logger.warning("Loading handlers for scheduler")

    dp = DjangoTelegramBot.dispatcher
    dp.add_handler(CommandHandler("my_events", registered_events_left))
    dp.add_handler(CommandHandler("lections", lections_left))
    dp.add_handler(CommandHandler("events", all_events_left))
    dp.add_handler(CommandHandler("full_schedule", all_schedule))