from larp_in_ua.apps.accounts.selectors import get_user_by_telegram_id


def get_help_message(update):
    user = get_user_by_telegram_id(update.message.chat_id)
    if not user:
        help_text = """
        Вітаю вас на конвенті! Щоб почати роботу, будь ласка, надішліть мені повідомлення
/register [email]
де замість [email] вкажіть ту адресу електронної пошти, яку ви вказували при реєстрації на поток "Діло". Якщо ви не реєструвалися на "Діло" просто вкажіть свою пошту; обіцяємо, що не будемо надсилати вам нічого з того, чого б ви не хотіли!
        """
    else:
        help_text = """
        Привіт, друзяко! Усе пучком? Якщо щось пішло не так - наприклад, ти не отримав найсвіжіших даних про лекції чи поток "Діло", - будь ласка, знайди Тенгро, він усе порулить у реалі; я ж просто бот, моя справа маленька.
        """
    return help_text
