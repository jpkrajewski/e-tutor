from datetime import datetime, timedelta
from time import time
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

def get_lessons_to_display(queryset, week='current'):
    """
    returns lessons in format -> {'Monday': [<QuerySet>], 'Tuesday': [<QuerySet>] ... ect}
    """
    now = datetime.now()
    start = now - timedelta(days=now.weekday())
    end = start + timedelta(days=6)

    start = start.replace(hour=0, minute=0)
    end = end.replace(hour=23, minute=59)

    if week == 'next':
        start += timedelta(days=7)
        end += timedelta(days=7)

    queryset = queryset.filter(start_datetime__range=(start, end)).annotate(weekday=Extract('start_datetime', 'iso_week_day'), hour=Extract(
        'start_datetime', 'hour')).order_by('weekday')
    lessons_in_day = []
    for iso in range(1, 8):
        lessons_in_day.append(queryset.filter(weekday=iso))

    return {x[0]: x[1] for x in zip(ISO_WEEK_DAYS, lessons_in_day)}
