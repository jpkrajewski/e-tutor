from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Lesson(models.Model):
    lesson_start_datetime = models.DateTimeField()
    lesson_end_datetime = models.DateTimeField()
    student_name = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    tutor_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.start_datetime


class TeachingRoom(models.Model):
    room_url = models.CharField(max_length=300)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class LessonNotes(models.Model):
    path = models.CharField(max_length=200)
    

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

