from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Student(models.Model):
    name = models.CharField(max_length=50)
    education_level = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    facebook_profile = models.CharField(max_length=150, blank=True)
    facebook_psid = models.CharField(max_length=50, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LessonNote(models.Model):
    path = models.CharField(max_length=200)


class LessonManager(models.Manager):
    def incoming_lessons(self, hours, tutor_id):
        now = datetime.now()
        return self.filter(lesson_start_datetime__gte=now,
                           lesson_start_datetime__lte=now + timedelta(hours=hours),
                           tutor_id=tutor_id)

    def get_done_lessons(self):
        return self.filter(lesson_end_datetime__lt=datetime.now())


class Lesson(models.Model):
    lesson_start_datetime = models.DateTimeField()
    lesson_end_datetime = models.DateTimeField()
    description = models.CharField(max_length=600, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    objects = LessonManager()

    class Meta:
        ordering = ['lesson_start_datetime']

    def __str__(self):
        return str(self.lesson_start_datetime) + " " + self.student.name


class TeachingRoom(models.Model):
    room_url = models.CharField(max_length=300)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class FacebookMessage(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=200)
    sender_psid = models.CharField(max_length=50)
    request_data = models.CharField(max_length=400)


class Task(models.Model):
    description = models.CharField(max_length=500)
    is_starred = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=datetime.now())
    category = models.PositiveSmallIntegerField(default=0)
    is_done = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['is_starred', 'is_done', '-start_date']

    def __str__(self):
        return self.description

