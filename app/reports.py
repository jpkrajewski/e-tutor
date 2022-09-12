from django.db.models import Sum
from datetime import datetime, time, timedelta


def get_students_missing_payments(queryset):
    """
    Students queryset
    """
    return (queryset
            .annotate(missing_payment=Sum('payment__amount'))
            .values('id', 'first_name', 'last_name', 'missing_payment')
            .exclude(missing_payment=None))


def get_total_student_missing_payment(queryset) -> int:
    """
    Student payments queryset
    """
    return queryset.aggregate(missing_payment=Sum('amount'))['missing_payment']


def get_lessons_today_and_tomorrow(queryset):
    """
    Tutor lessons queryset
    """
    start_of_a_day = datetime.combine(datetime.today(), time.min)
    end_of_a_tomorrow = datetime.combine(datetime.today(), time.max) + timedelta(days=1)

    return queryset.filter(start_datetime__range=(start_of_a_day, end_of_a_tomorrow))


def get_money_per_week(queryset):
    """
    Tutor lessons queryset
    """

    return queryset.filter()