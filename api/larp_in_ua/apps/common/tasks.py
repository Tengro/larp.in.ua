from larp_in_ua import celery_app
import requests
from django_telegrambot.apps import DjangoTelegramBot


@celery_app.task
def refresh_hook():
    token = DjangoTelegramBot.dispatcher.bot.token
    requests.get(f"https://api.telegram.org/bot{token}/setWebhook?url=https://tengro.site/bot/{token}/")


@celery_app.task
def heartbeat():
    user = UserAccount.objects.get_tengro_account()
    user.send_message("ITS ALIVE")
