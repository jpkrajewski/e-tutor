from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone


class Tutor(models.Model):
    avatar_img_path = models.CharField(max_length=300, blank=True)
    psid = models.IntegerField()
    send_reminder_hours_before = models.IntegerField(default=1)
    send_reminders_to_yourself = models.BooleanField(default=False)
    send_reminders_to_students = models.BooleanField(default=False)
    message_template_to_yourself = models.CharField(max_length=500, blank=True)
    message_template_to_students = models.CharField(max_length=500, blank=True)
    account_active = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    education_level = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
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
                           facebook_notification_send=False)

    def get_lessons_ready_for_creating_teaching_room(self, datetime_now):
        return self.filter(start_datetime__gte=datetime_now,
                           start_datetime__lte=datetime_now + timedelta(hours=1)) \
            .exclude(pk__in=[x.lesson.pk for x in TeachingRoom.objects.all()])

    def get_done_lessons(self):
        return self.filter(end_datetime__lt=datetime.now(tz=timezone.utc))


class Lesson(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    description = models.CharField(max_length=600, blank=True)
    repetitive = models.BooleanField(default=True)
    send_reminder = models.BooleanField(default=True)
    facebook_notification_send = models.BooleanField(default=False)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = LessonManager()

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return str(self.start_datetime.astimezone()) + " " + self.student.first_name + ' ' + self.student.last_name

    def get_absolute_url(self):
        return reverse('lesson-detail', args=[self.id])


class TeachingRoom(models.Model):
    url = models.CharField(max_length=300)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('teaching-room', args=[self.url])


class FacebookMessage(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=200)
    sender_psid = models.CharField(max_length=50)
    request_data = models.CharField(max_length=400)
