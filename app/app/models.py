from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    discord_nick = models.CharField(max_length=50, blank=True)
    facebook_profile = models.CharField(max_length=150, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def get_absolute_url(self):
        return reverse("student-detail", args=[self.id])


class Payment(models.Model):
    PAID = "paid"
    DUE = "due"

    STATUS = [(PAID, _("Paid")), (DUE, _("Payment due"))]

    lesson_date = models.DateTimeField()
    amount = models.PositiveIntegerField(null=False, blank=False)
    status = models.CharField(max_length=30, choices=STATUS, default=DUE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    @property
    def date(self):
        return self.lesson_date.astimezone().strftime("%d.%m.%Y")

    def change_status_to_paid(self):
        self.status = self.PAID


class LessonManager(models.Manager):
    def get_lessons_for_reminders(self):
        now = datetime.now(tz=timezone.utc)
        return self.filter(
            start_datetime__gte=now, start_datetime__lte=now + timedelta(hours=3)
        ).filter(is_notification_send=False)

    def get_done_lessons(self):
        return self.filter(end_datetime__lt=datetime.now(tz=timezone.utc))


class Lesson(models.Model):
    ONLINE = "Online"
    AT_CLIENTS = "Client's"
    AT_TUTORS = "Tutor's"
    PLACE = [
        (ONLINE, _("Online")),
        (AT_CLIENTS, _("Client's")),
        (AT_TUTORS, _("Tutor's")),
    ]
    subject = models.CharField(max_length=50)
    place = models.CharField(max_length=30, choices=PLACE, default=ONLINE)
    amount = models.PositiveIntegerField(null=False, blank=False)
    description = models.CharField(max_length=250, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_repetitive = models.BooleanField(default=True)
    is_notification_send = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    objects = LessonManager()

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return f'{self.start_datetime.astimezone().strftime("%A, %m/%d/%Y, %H:%M")} {self.student.first_name} {self.student.last_name}'

    def get_lesson_start_and_end_time(self) -> str:
        return "{start} - {end}".format(
            start=self.start_datetime.astimezone().strftime("%H:%M"),
            end=self.end_datetime.astimezone().strftime("%H:%M"),
        )

    @property
    def start_date(self) -> str:
        return self.start_datetime.astimezone().strftime("%A, %d.%m.%Y")

    @property
    def start_hour(self):
        return self.start_datetime.astimezone().strftime("%H:%M")

    @property
    def end_hour(self):
        return self.end_datetime.astimezone().strftime("%H:%M")

    def get_absolute_url(self) -> str:
        return reverse("lesson-detail", args=[self.id])


class TeachingRoomManager(models.Manager):
    def get_inactive(self):
        return self.filter(lesson__end_datetime__lt=datetime.now(tz=timezone.utc))


class TeachingRoom(models.Model):
    url = models.CharField(max_length=300)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    objects = TeachingRoomManager()

    def __str__(self):
        return self.lesson.student.first_name

    def get_absolute_url(self):
        return f"{settings.LESSON_URL}{reverse('teaching-room', args=[self.url])}"
