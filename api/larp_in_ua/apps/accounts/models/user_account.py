from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from larp_in_ua.apps.common.utils.safe_send import safe_message_send
from django_telegrambot.apps import DjangoTelegramBot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from larp_in_ua.apps.common import models as core_models
from larp_in_ua.apps.common.models import CoreModel
from larp_in_ua.apps.scheduler.models import RegistrationStatus


class UserManager(core_models.CoreManager, BaseUserManager):
    def get_queryset(self):
        return core_models.CoreQuerySet(self.model, using=self._db)

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must give an email address")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def get_tengro_account(self):
        return self.get_queryset().filter(is_tengro=True).first()


class UserAccount(PermissionsMixin, CoreModel, AbstractBaseUser):

    email = models.EmailField(verbose_name=gettext_lazy("Email"), max_length=128, unique=True)
    first_name = models.CharField(verbose_name=gettext_lazy("first name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(verbose_name=gettext_lazy("last name"), max_length=30, blank=True, null=True)
    telegram_id = models.CharField(verbose_name=gettext_lazy("Telegram ID"), max_length=128, blank=True, null=True)
    is_tengro = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy("Designates if it's superduper admin."),
    )
    is_staff = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        gettext_lazy("active (is fully registered)"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return self.email

    def get_short_name(self) -> str:
        return str(self.email)

    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
        elif self.first_name:
            full_name = f"{self.first_name}"
        else:
            full_name = self.get_short_name()
        return full_name

    @property
    def notification_salutation(self):
        if self.first_name and self.last_name:
            salutation = f"{self.first_name} {self.last_name}"
        else:
            salutation = gettext_lazy("Dear guest!")
        return salutation

    def send_message(self, text):
        if self.telegram_id:
            dp = DjangoTelegramBot.dispatcher.bot
            safe_message_send(dp, self.telegram_id, str(text))

    def send_registration_message(self):
        message_text = """
Отепер - привіт, друже! Мене звати Говард, я перший бот-хамелеон цього конвенту і я допоможу тобі не заблукати.

Якщо ти рєеструвалася (чи рєеструвався) на щось з потоку "Діло", я нагадаю тобі про цей івент за пів-години до старту, але тобі треба буде протягом двадцятити п'яти хвилин підтвердити свою участь, інакше мені доведеться вважати, що тебе на івенті не буде.

Якщо ти у списку очікування кудись, то я швиденько порадую тебе новинами, якщо з'явиться вільне місце, але знову ж, тобі треба буде швидко (за дві хвилини) підтвердити свої наміри.

Усім цим сьогодні займатимусь саме я, Говард, бот-хамелеон, а не хтось з організаторів, але якщо трапиться якась халепа - знайди їх у реальному просторі. Вони допоможуть.
        """
        self.send_message(message_text)

    def send_personal_schedule(self):
        from larp_in_ua.apps.scheduler.selectors import get_registered_events, get_waitlisted_registered_events
        registered_events = get_registered_events(self)
        waitlisted_events = get_waitlisted_registered_events(self)
        if registered_events:
            self.send_message("Тебе зареєстровано на наступні події потоку \"Діло\":")
            for event_invitiation in registered_events:
                self.send_message(f"{event_invitiation.event.title} о {event_invitiation.event.time_string}")
        if waitlisted_events:
            self.send_message("Ти у списку очікування на наступні події потоку \"Діло\":")
            for event_invitiation in waitlisted_events:
                self.send_message(f"{event_invitiation.event.title} о {event_invitiation.event.time_string}")

    def send_approval_request(self, closest_workshop_invite, is_waitlist=False):
        closest_workshop = closest_workshop_invite.event
        if not self.telegram_id:
            return
        if is_waitlist:
            text = closest_workshop.workshop_invitation_hot
        else:
            text = closest_workshop.workshop_invitation
        dp = DjangoTelegramBot.dispatcher.bot
        approve_button = InlineKeyboardButton("\u2705 Так, буду", callback_data=f"{RegistrationStatus.APPROVED}|||{closest_workshop_invite.pk}|||{is_waitlist}")
        decline_button = InlineKeyboardButton("\u274C Ні, не зможу", callback_data=f"{RegistrationStatus.DECLINED}|||{closest_workshop_invite.pk}|||{is_waitlist}")
        markup = InlineKeyboardMarkup([[approve_button, decline_button]], one_time_keyboard=True)
        dp.sendMessage(self.telegram_id, text, reply_markup=markup)
