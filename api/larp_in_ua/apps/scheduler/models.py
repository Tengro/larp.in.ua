from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy
from larp_in_ua.apps.common.models import CoreModel
from larp_in_ua.apps.scheduler.constants import MAX_TIMES_ASKED, MAX_TIMES_ASKED_HOT

import logging
logger = logging.getLogger(__name__)


class EventTypeChoices(models.IntegerChoices):
    LECTURE = 1, "Івент потоку \"Слово\""
    WORKSHOP = 2, "Івент потоку \"Діло\""
    NIGHT = 3, "Івент Do!Roleplay Night"


class EventLaneChoices(models.IntegerChoices):
    FIRST_LANE = 1, "Великий"
    SECOND_LANE = 2, "Малий"


class NightEventLaneChoices(models.IntegerChoices):
    GREAT_HALL = 1, "Великий"
    CUDDLE = 2, "Party Room: Cuddle-puddle"
    LOCK_STOCK_BARRELS = 3, "Party Room: Карти, гроші, два стволи"
    CYBERPUNK_TRAP = 4, "Party Room: CYBERPUNK#TRAP"
    ORG_LOCATION = 5, "Організаторське приміщення"


class Event(CoreModel):
    event_time = models.DateTimeField()
    event_type = models.IntegerField(
        choices=EventTypeChoices.choices,
    )
    title = models.CharField(max_length=256)
    organizers = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    maximal_participants = models.IntegerField()
    event_lane = models.IntegerField(
        choices=EventLaneChoices.choices,
        blank=True,
        null=True,
    )
    night_event_lane = models.IntegerField(
        choices=NightEventLaneChoices.choices,
        blank=True,
        null=True,
    )
    finished_notification = models.BooleanField(default=False)

    @property
    def time_string(self):
        event_time = timezone.localtime(self.event_time)
        return event_time.strftime("%H:%M")

    @property
    def lection_representation(self) -> str:
        resulting_string = "Нагадуємо!\nО {time} відбудеться івент потоку \"Слово\" від {organizers}. Реєсстрація не потрібна!\n<b>Назва івенту</b>: {name}\n<b>Опис</b>: {description}".format(
            time=self.time_string,
            organizers=self.organizers,
            name=self.title,
            description=self.description
        )
        return resulting_string

    @property
    def night_representation(self) -> str:
        resulting_string = "Увага!\nО {time} у {label} відбудеться івент від {organizers}. !\n<b>Назва івенту</b>: {name}".format(
            time=self.time_string,
            organizers=self.organizers,
            name=self.title,
            label=self.get_night_event_lane_display(),
        )
        return resulting_string

    @property
    def workshop_invitation(self) -> str:
        resulting_string = """
О {time} відбудеться івент потоку \"Діло\" від {organizers}.
<b>Назва</b>: {name}
<b>Опис</b>: {description}
Підтверьдте участь!
Якщо протягом 25 хвилин ви не відповісте на це запрошення, ваше місце на івенті перейде комусь зі списку очікіування.
        """.format(
            time=self.time_string,
            organizers=self.organizers,
            name=self.title,
            description=self.description
        )
        return resulting_string

    @property
    def workshop_invitation_hot(self) -> str:
        resulting_string = """
Привіт! У нас хороші новини.
О {time} відбудеться івент потоку \"Діло\" від {organizers}.
<b>Назва</b>: {name}
<b>Опис</b>: {description}
Ви були у списку очікування цього івенту - і зараз з'явилося вільне місце!
Якщо протягом 2 хвилин ви не відповісте на це запрошення, ваше місце на івенті перейде комусь іще зі списку очікіування.
        """.format(
            time=self.time_string,
            organizers=self.organizers,
            name=self.title,
            description=self.description
        )
        return resulting_string

    def ffa_notification(self, places) -> str:
        resulting_string = """
УВАГА! УВАГА! УВАГА!
Ось-ось, о {time} відбудеться івент потоку \"Діло\" від {organizers}
Цей івент відбудеться на локації {label} потік "Діло"
<b>Назва</b>: {name}
<b>Опис</b>: {description}
За нашими даними, на цей івент з'явилися вільні місця (хтось з тих, хто реєструвався попередньо, не підтвердив участі).
Всього {places} місць!
Зверніться до організаторів, можливо вони чекають саме на вас!
        """.format(
            time=self.time_string,
            organizers=self.organizers,
            name=self.title,
            description=self.description,
            places=places,
            label=self.get_event_lane_display(),
        )
        return resulting_string

    def __str__(self, *args, **kwargs):
        return f"{self.title} о {self.time_string} від {self.organizers}"

    class Meta:
        ordering = ('event_time',)


class RegistrationStatus(models.IntegerChoices):
    ON_HOLD = 1, "У черзі"
    PRE_APPROVED = 2, "Участь попередньо підтверджено"
    APPROVED = 3, "Участь підтверджено"
    DECLINED = 4, "Участь відхилено"
    BANNED = 5, "Не допущено за проханням організатора"


class EventRegistration(CoreModel):
    user = models.ForeignKey('accounts.UserAccount', related_name='registered_events', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='registered_users', on_delete=models.CASCADE)
    registration_status = models.IntegerField(
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.ON_HOLD
    )
    _was_invited = models.BooleanField(default=False)
    _times_asked = models.IntegerField(default=0)

    def __str__(self, *args, **wargs):
        return f"{self.event.title} о {self.event.time_string}: реєстрація для {self.user.email}"

    class Meta:
        ordering = ('created',)

    def send_approval_request(self, is_hot):
        self.user.send_approval_request(self, is_hot)

    def process_invite(self, status, is_hot):
        is_hot = bool(is_hot)
        max_counter = MAX_TIMES_ASKED_HOT if is_hot else MAX_TIMES_ASKED
        full_stop = False
        if self.registration_status in [RegistrationStatus.APPROVED, RegistrationStatus.DECLINED]:
            text = "Схоже, ви вже відповіли на запрошення на цей івент!"
            full_stop = True
        if self._times_asked > max_counter:
            text = "Схоже, ви не відповіли вчасно і пропустили дедлайн =("
            full_stop = True
        if self.event.finished_notification:
            text = "Схоже на цей івент вже не збирають підтверджень; він або ось-ось почнеться, або набрав повний список"
            full_stop = True
        if self.event.event_time < now():
            full_stop = True
            text = "Схоже, івент вже почався і ви пропустили дедлайн =("
        if full_stop:
            return text
        self.registration_status = status
        self.save()
        approved = int(status) == int(RegistrationStatus.APPROVED.value)
        declined = int(status) == int(RegistrationStatus.DECLINED.value)
        if approved:
            text = 'Дякуємо за відповідь! Очікуємо вас на івенті!'
        if declined:
            text = 'Дякуємо за відповідь! Шкода, що не вийшло.'
        return text
