from django.db.models.functions import Extract


def order_lessons_by_weekday_and_hours(queryset):
    """
    returns {'Monday': [<QuerySet>], 'Tuesday': [<QuerySet>] ... ect}
    """

    queryset = queryset.annotate(weekday=Extract('start_datetime', 'iso_week_day'), hour=Extract(
        'start_datetime', 'hour')).order_by('weekday')
    lessons_in_day = []
    for iso in range(1, 8):
        lessons_in_day.append(queryset.filter(weekday=iso))

    iso_week_days = (
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
    )

    return {x[0]: x[1] for x in zip(iso_week_days, lessons_in_day)}
