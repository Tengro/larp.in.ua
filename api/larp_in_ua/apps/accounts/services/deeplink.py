from larp_in_ua.apps.accounts.selectors import get_user_by_email, get_user_by_telegram_id
from larp_in_ua.apps.accounts.models.user_account import UserAccount
import re


def bind_user(update):
    created = False
    match = re.search(r'([\w.-]+)@([\w.-]+)', update.message.text)
    if not match:
        return (False, "E-mail вказано невірно. Перевірте введені дані", False)

    email = match.group()
    telegram_id = update.message.chat_id
    if telegram_id < 0:
        return (False, "Напишіть боту у особисті повідомлення, а не в спільний чат.", False)
    tg_user = get_user_by_telegram_id(telegram_id)
    if tg_user is not None:
        return (False, "Користувача з вашого аккаунту TG уже зареєстровано", False)

    user = UserAccount.objects.filter(email=email).first()
    if not user:
        user = UserAccount.objects.create_user(email=email)
        user.is_active = True
        user.save()
        created = True
    if user.telegram_id is not None:
        return (False, "Користувача з таким e-mail уже зареєстровано", False)

    user.telegram_id = telegram_id
    user.save()
    return (True, user, created)
