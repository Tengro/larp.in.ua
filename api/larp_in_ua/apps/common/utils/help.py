from larp_in_ua.apps.accounts.selectors import get_user_by_telegram_id


def get_help_message(update):
    user = get_user_by_telegram_id(update.message.chat_id)
    if not user:
        help_text = """
        blahblah unreg
        """
    else:
        help_text = """
        blahblah reged
        """
    return help_text
