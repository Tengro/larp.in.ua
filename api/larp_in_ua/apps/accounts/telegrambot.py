from telegram.ext import CommandHandler, CallbackQueryHandler
from django_telegrambot.apps import DjangoTelegramBot

from larp_in_ua.apps.accounts.services.deeplink import bind_user
from larp_in_ua.apps.accounts.selectors import get_user_by_telegram_id
from larp_in_ua.apps.common.utils.help import get_help_message
from larp_in_ua.apps.common.utils.safe_send import safe_message_send
from larp_in_ua.apps.scheduler.models import EventRegistration


import logging
logger = logging.getLogger(__name__)


def help(update, context):
    help_message = get_help_message(update)
    safe_message_send(context.bot, update.message.chat_id, text=help_message)


def register(update, context):
    success, result, is_created = bind_user(update)
    if not success:
        safe_message_send(context.bot, update.message.chat_id, text=result)
        return
    result.send_registration_message()
    result.send_personal_schedule()


def button(update, context) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    status, item_id, is_waitlist = query.data.split('|||')
    invitation = EventRegistration.objects.get(pk=item_id)
    text = invitation.process_invite(status, is_waitlist)
    safe_message_send(context.bot, query.message.chat_id, text=text)
    query.answer(text)


def error(update, context):
    from larp_in_ua.apps.accounts.models import UserAccount
    user = UserAccount.objects.get_tengro_account()
    if update.message:
        message_text = update.message.text
        telegram_id = update.message.chat_id
        caused = get_user_by_telegram_id(telegram_id)
        user.send_message(f"Update {message_text} from {caused} resulted in exception: {context.error}")
    else:
        user.send_message(f"Error {context.error}")
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def registered_events_left(update, context):
    telegram_id = update.message.chat_id
    result = get_user_by_telegram_id(telegram_id)
    if result:
        result.send_personal_schedule()
    else:
        safe_message_send(context.bot, update.message.chat_id, text="Здається, ви ще не зареєструвалися?")


def main():
    logger.warning("Loading handlers for registration")

    dp = DjangoTelegramBot.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CallbackQueryHandler(button))
    # log all errors
    dp.add_error_handler(error)
