from larp_in_ua.apps.scheduler.selectors import all_events, events_left, get_all_lections, lections_left
from larp_in_ua.apps.scheduler.models import EventLaneChoices


def prepare_events_all():
    return [f'Потік "Діло", {t}\n\n,' + '\n\n'.join([x.__str__() for x in y]) for t, y in all_events() if y]


def prepare_events_left():
    return [f'Потік "Діло", {t}\n\n' + '\n\n'.join([x.__str__() for x in y]) for t, y in events_left() if y]


def prepare_lections_all():
    return 'Потік "Слово"\n\n' + '\n\n'.join([x.__str__() for x in get_all_lections()])


def prepare_lections_left():
    data = '\n\n'.join([x.__str__() for x in lections_left()])
    if data:
        return 'Потік "Слово"\n\n' + data
    return "Здається, потік \"Слово\" добігає кінця!"
