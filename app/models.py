from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Tutor(models.Model):
    avatar_img_path = models.CharField(max_length=300, blank=True)
    facebook_psid = models.CharField(max_length=50)
    send_reminder_hours_before = models.IntegerField(default=1)
    send_reminders_to_yourself = models.BooleanField(default=False)
    send_reminders_to_students = models.BooleanField(default=False)
    message_template_to_yourself = models.CharField(max_length=500, blank=True)
    message_template_to_students = models.CharField(max_length=500, blank=True)
    account_active = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    @property
    def int_facebook_psid(self):
        return int(self.facebook_psid)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    discord_nick = models.CharField(max_length=50, blank=True)
    facebook_profile = models.CharField(max_length=150, blank=True)
    facebook_psid = models.CharField(max_length=50, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('student-detail', args=[self.id])


class LessonManager(models.Manager):
    def get_lessons_for_reminders(self, hours_before, datetime_now):
        return self.filter(start_datetime__gte=datetime_now,
                           start_datetime__lte=datetime_now + timedelta(hours=hours_before),
                           is_facebook_notification_send=False)

    def get_lessons_ready_for_creating_teaching_room(self, datetime_now):
        return (
                self.filter(start_datetime__gte=datetime_now,
                            start_datetime__lte=datetime_now + timedelta(hours=1),
                            place=Lesson.ONLINE)
                    .exclude(pk__in=[x.lesson.pk for x in TeachingRoom.objects.all()])
                )

    def get_done_lessons(self):
        return self.filter(end_datetime__lt=datetime.now(tz=timezone.utc), is_repetitive=True)


class Lesson(models.Model):
    ONLINE = 'online'
    AT_CLIENTS = 'client'
    AT_TUTORS = 'tutor'
    PLACE = [
        (ONLINE, _('Online')),
        (AT_CLIENTS, _("At client's place")),
        (AT_TUTORS, _("At tutor's place")),
    ]

    subject = models.CharField(max_length=50)
    place = models.CharField(max_length=30, choices=PLACE, default=ONLINE)
    money_per_hour = models.PositiveIntegerField(null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    description = models.CharField(max_length=250, blank=True)
    is_repetitive = models.BooleanField(default=True)
    is_sending_reminder = models.BooleanField(default=True)
    is_facebook_notification_send = models.BooleanField(default=False)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = LessonManager()

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return self.start_datetime.astimezone().strftime("%m/%d/%Y, %H:%M") + ' ' + self.student.first_name + ' ' + self.student.last_name

    def get_absolute_url(self):
        return reverse('lesson-detail', args=[self.id])


class TeachingRoom(models.Model):
    url = models.CharField(max_length=300)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson.student.first_name

    def get_absolute_url(self):
        return reverse('teaching-room', args=[self.url])


class FacebookMessage(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=200)
    sender_psid = models.CharField(max_length=50)
    request_data = models.CharField(max_length=400)
