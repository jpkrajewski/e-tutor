from datetime import datetime, timedelta, timezone

from django.test import TestCase

from app.factories.lessons_factory import LessonFactory
from app.factories.payment_factory import PaymentFactory
from app.factories.students_factory import StudentFactory
from app.factories.tutor_factory import TutorFactory
from app.utils.reports import (
    get_lessons_today_and_tomorrow,
    get_money_per_week,
    get_students_missing_payments,
)


class TestReportsMissingPayments(TestCase):
    def setUp(self):
        self.tutor = TutorFactory()
        self.expected_missing_payment = 0
        amount = 100
        for _ in range(3):
            student = StudentFactory(tutor=self.tutor)
            for _ in range(3):
                self.expected_missing_payment += amount
                PaymentFactory(student=student, amount=amount, status="due")

    def test_get_students_missing_payments(self):
        self.maxDiff = None
        students = get_students_missing_payments(self.tutor.student_set.all())
        missing_payments = sum([student["missing_payment"] for student in students])
        self.assertEqual(missing_payments, self.expected_missing_payment)


class TestReportsLessonsTodayAndTomorrow(TestCase):
    def setUp(self) -> None:
        self.tutor = TutorFactory()
        self.student = StudentFactory(tutor=self.tutor)
        date = datetime.now(tz=timezone.utc)
        for _ in range(3):
            LessonFactory(
                tutor=self.tutor,
                student=self.student,
                start_datetime=date - timedelta(hours=10),
                end_datetime=date - timedelta(hours=11),
            )
        for _ in range(3):
            LessonFactory(
                tutor=self.tutor,
                student=self.student,
                start_datetime=date
                + timedelta(hours=1),  # We only get lessons that are incoming
                end_datetime=date + timedelta(hours=2),
            )
        for _ in range(3):
            LessonFactory(
                tutor=self.tutor,
                student=self.student,
                start_datetime=date + timedelta(hours=20),
                end_datetime=date + timedelta(hours=21),
            )

    def test_get_lessons_today_and_tomorrow(self):
        lessons = get_lessons_today_and_tomorrow(self.tutor.lesson_set.all())
        self.assertEqual(lessons.count(), 6)


class TestReportsMoenyPerWeek(TestCase):
    def setUp(self) -> None:
        self.tutor = TutorFactory()
        self.student = StudentFactory(tutor=self.tutor)
        date = datetime.now(tz=timezone.utc)
        self.expected_amount = 0
        amount = 50
        for _ in range(3):
            LessonFactory(
                tutor=self.tutor,
                student=self.student,
                amount=amount,
                start_datetime=date,
                end_datetime=date,
            )
            self.expected_amount += amount
        for _ in range(3):  # This lessons are not in the same week
            LessonFactory(
                tutor=self.tutor,
                student=self.student,
                amount=1,
                start_datetime=date + timedelta(days=30),
                end_datetime=date + timedelta(days=30),
            )

    def test_get_money_per_week(self):
        money_per_week = get_money_per_week(self.tutor.lesson_set.all())
        self.assertEqual(money_per_week, self.expected_amount)
