from larp_in_ua import celery_app
from django.utils.timezone import now
from larp_in_ua.apps.accounts.selectors import get_all_users
from larp_in_ua.apps.scheduler.selectors import (
    get_closest_lection, get_closest_not_filled_workshop,
)
from larp_in_ua.apps.scheduler.models import RegistrationStatus, EventLaneChoices
from larp_in_ua.apps.scheduler.constants import MAX_TIMES_ASKED_HOT, MAX_TIMES_ASKED, FREE_FOR_ALL_TIME, LAST_TIME_SET


@celery_app.task
def notify_closest_lection():
    closest_lection = get_closest_lection()
    if closest_lection:
        all_users = get_all_users()
        for user in all_users:
            user.send_message(closest_lection.lection_representation)
        closest_lection.finished_notification = True
        closest_lection.save()


@celery_app.task
def notify_closest_events():
    for choice in EventLaneChoices.choices:
        this_time = now()
        closest_workshop = get_closest_not_filled_workshop(choice[0])
        if not closest_workshop:
            continue
        prepared_users = closest_workshop.registered_users.filter(registration_status=RegistrationStatus.PRE_APPROVED)
        free_slots = closest_workshop.maximal_participants - closest_workshop.existing_participants - prepared_users.count()
        waiting_users = closest_workshop.registered_users.filter(registration_status=RegistrationStatus.ON_HOLD)
        ffa_time = ((closest_workshop.event_time - this_time).seconds/60) < FREE_FOR_ALL_TIME

        selected_waiting_users = waiting_users[:free_slots]

        for user in prepared_users:
            user._times_asked += 1
            if user._times_asked > MAX_TIMES_ASKED:
                user.registration_status = RegistrationStatus.DECLINED
                user.save()
                user.send_message("Вашу реєстрацію на івент відмінено через брак вчасної відповіді")
                continue
            if not user._was_invited:
                user._was_invited = True
                user.send_approval_request(False)
                user.save()
        last_call_for_waitlist = ((closest_workshop.event_time - this_time).seconds/60) < LAST_TIME_SET
        if last_call_for_waitlist:
            for user in selected_waiting_users:
                user._times_asked += 1
                if user._times_asked > MAX_TIMES_ASKED_HOT:
                    user.registration_status = RegistrationStatus.DECLINED
                    user.save()
                    user.send_message("Вашу реєстрацію на івент відмінено через брак вчасної відповіді")
                    continue
                if not user._was_invited:
                    user._was_invited = True
                    user.send_approval_request(True)
                    user.save()

        if (free_slots > 0 and ffa_time) or (not prepared_users and not waiting_users and free_slots > 0 and last_call_for_waitlist):
            free_users = list(waiting_users) + list(get_all_users().exclude(registered_events__event=closest_workshop))
            for user in free_users:
                user.send_message(closest_workshop.ffa_notification(free_slots))

        if ffa_time:
            closest_workshop.finished_notification = True
            closest_workshop.save()
            continue
