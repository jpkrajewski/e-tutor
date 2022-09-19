from django.db.models import Sum
from django.utils import timezone

from datetime import datetime, time, timedelta
from .models import Payment


def get_students_missing_payments(queryset):
    """
    Students queryset
    """
    return (queryset
            .filter(payment__status=Payment.DUE)
            .annotate(missing_payment=Sum('payment__amount'))
            .values('first_name', 'last_name', 'missing_payment')
            .exclude(missing_payment=None))

def get_student_missing_payment(queryset):
    return (queryset
            .filter(status=Payment.DUE)
            .annotate(missing_payment=Sum('amount')))

def get_total_student_missing_payment(queryset) -> int:
    """
    Student payments queryset
    """
    return queryset.filter(status=Payment.DUE).aggregate(missing_payment=Sum('amount'))['missing_payment']


def get_lessons_today_and_tomorrow(queryset):
    """
    Tutor lessons queryset
    """
    start_of_a_day = datetime.combine(datetime.today(), time.min)
    end_of_a_tomorrow = datetime.combine(
        datetime.today(), time.max) + timedelta(days=1)

    return queryset.filter(start_datetime__range=(start_of_a_day, end_of_a_tomorrow)).filter(start_datetime__gte=datetime.now(tz=timezone.utc))


def get_money_per_week(queryset) -> int:
    """
    Tutor lessons queryset
    """
    now = datetime.now(tz=timezone.utc)
    start = now - timedelta(days=now.weekday())
    end = start + timedelta(days=6)

    return queryset.filter(start_datetime__range=(start, end)).aggregate(money_weekly=Sum('amount'))['money_weekly']
