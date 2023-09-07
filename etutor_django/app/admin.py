from django.contrib import admin
from app.models import Student, Lesson, Tutor, TeachingRoom, Payment

# Register your models here.

admin.site.register([Payment, Student, Lesson, Tutor, TeachingRoom])
