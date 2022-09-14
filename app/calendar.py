from datetime import datetime, timedelta
from django.db.models.functions import Extract


ISO_WEEK_DAYS = (
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
    )

def order_lessons_from_this_week_by_days_and_hours(queryset):
    """
    returns lessons from current weekend in format -> {'Monday': [<QuerySet>], 'Tuesday': [<QuerySet>] ... ect}
    """
    now = datetime.now()
    start = now - timedelta(days=now.weekday())
    end = start + timedelta(days=6)

    return _order_transform_lessons(queryset, start, end)


def order_lessons_from_next_week_by_days_and_hours(queryset):
    """
    returns lessons from next weekend in format -> {'Monday': [<QuerySet>], 'Tuesday': [<QuerySet>] ... ect}
    """
    now = datetime.now()
    start = now - timedelta(days=now.weekday()) + timedelta(days=7)
    end = start + timedelta(days=6) + timedelta(days=7)

    return _order_transform_lessons(queryset, start, end)


def _order_transform_lessons(queryset, start, end):
    queryset = queryset.filter(start_datetime__range=(start, end)).annotate(weekday=Extract('start_datetime', 'iso_week_day'), hour=Extract(
        'start_datetime', 'hour')).order_by('weekday')
    lessons_in_day = []
    for iso in range(1, 8):
        lessons_in_day.append(queryset.filter(weekday=iso))

    return {x[0]: x[1] for x in zip(ISO_WEEK_DAYS, lessons_in_day)}