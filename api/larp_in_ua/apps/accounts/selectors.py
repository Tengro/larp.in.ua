from typing import Optional
from django.db.models import Q, QuerySet
from larp_in_ua.apps.accounts.models import UserAccount


def get_all_users() -> QuerySet:
    return UserAccount.objects.active()


def get_user_by_email(email: str) -> Optional[UserAccount]:
    return UserAccount.objects.active().filter(character_id=character_id).first()


def get_all_admins() -> QuerySet:
    return UserAccount.objects.filter(Q(is_staff=True) | Q(is_superuser=True))


def get_user_by_telegram_id(telegram_id: str) -> UserAccount:
    return UserAccount.objects.active().filter(telegram_id=telegram_id).first()


def get_tengro_account() -> UserAccount:
    return UserAccount.objects.active().filter(is_superuser=True, is_tengro=True).first()
