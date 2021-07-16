import functools
from larp_in_ua.apps.accounts.selectors import get_user_by_telegram_id


def throttling_decorator(func):
    """
    THROTTLING
    """
    @functools.wraps(func)
    def wrapper_bot_function(update, context):
        requester = get_user_by_telegram_id(update.message.chat_id)
        if requester and requester.requests_made_since_last_purge > 100:
            requester.send_message("Перевищено ліміт запитів у систему. Ліміт скидається до нуля щопівгодини за місцевим часом")
            return
        else:
            if requester:
                requester.requests_made_since_last_purge += 1
                requester.save()
            return func(update, context)
    return wrapper_bot_function
