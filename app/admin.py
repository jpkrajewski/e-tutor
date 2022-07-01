from django.contrib import admin
from .models import Task, Student, Lesson, FacebookMessage

# Register your models here.

admin.site.register(Student)
admin.site.register(Task)
admin.site.register(Lesson)
admin.site.register(FacebookMessage)