from typing import Optional
from django.db.models import F, Q, Count, QuerySet
from django.utils.timezone import now
from datetime import timedelta
from larp_in_ua.apps.scheduler.models import (
    Event,
    EventTypeChoices,
    RegistrationStatus,
    EventRegistration,
    EventLaneChoices,
)

CLOSEST_TIME_IN_MINUTES = 30
CLOSEST_LECTURE_TIME_IN_MINUTES = 5


def get_all_lections() -> QuerySet:
    return Event.objects.filter(event_type=EventTypeChoices.LECTURE)


def get_closest_night_event() -> QuerySet:
    this_moment = now()
    closest_moment = now() + timedelta(minutes=CLOSEST_LECTURE_TIME_IN_MINUTES)
    return Event.objects.filter(event_type=EventTypeChoices.NIGHT).exclude(finished_notification=True).filter(event_time__range=(this_moment, closest_moment)).order_by('event_time').first()


def get_closest_lection() -> Optional[Event]:
    this_moment = now()
    closest_moment = now() + timedelta(minutes=CLOSEST_LECTURE_TIME_IN_MINUTES)
    lections = get_all_lections().exclude(finished_notification=True)
    closest_lection = lections.filter(event_time__range=(this_moment, closest_moment)).order_by('event_time').first()
    return closest_lection


def get_not_filled_workshops() -> QuerySet:
    all_workshops = Event.objects.filter(
        event_type=EventTypeChoices.WORKSHOP
    ).annotate(
        existing_participants=Count('registered_users', filter=Q(registered_users__registration_status=RegistrationStatus.APPROVED))
    )
    return all_workshops.filter(maximal_participants__gt=F('existing_participants'))


def get_closest_not_filled_workshop(lane_number):
    unfilled_workshops = get_not_filled_workshops().filter(event_lane=lane_number).exclude(finished_notification=True)
    this_moment = now()
    closest_moment = now() + timedelta(minutes=CLOSEST_TIME_IN_MINUTES)
    closest_workshop = unfilled_workshops.filter(event_time__range=(this_moment, closest_moment)).order_by('event_time').first()
    return closest_workshop


def get_registered_events(user_account):
    this_moment = now()
    return EventRegistration.objects.filter(
        user=user_account
    ).filter(
        registration_status=RegistrationStatus.PRE_APPROVED,
        event__event_time__gte=this_moment,
    ).select_related('event').order_by('event__event_time')


def get_waitlisted_registered_events(user_account):
    this_moment = now()
    return EventRegistration.objects.filter(
        user=user_account
    ).filter(
        registration_status=RegistrationStatus.ON_HOLD,
        event__event_time__gte=this_moment,
    ).select_related('event').order_by('event__event_time')


def all_events():
    result = []
    for choice in EventLaneChoices.choices:
        queryset = Event.objects.filter(event_type=EventTypeChoices.WORKSHOP).filter(event_lane=choice[0])
        title = choice[1]
        result.append((title, queryset))
    return result


def events_left():
    result = []
    this_moment = now()
    for choice in EventLaneChoices.choices:
        queryset = Event.objects.filter(event_type=EventTypeChoices.WORKSHOP).filter(event_lane=choice[0]).filter(event_time__gte=this_moment)
        title = choice[1]
        result.append((title, queryset))
    return result


def lections_left():
    this_moment = now()
    return get_all_lections().filter(event_time__gte=this_moment)
