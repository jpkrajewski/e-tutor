from django.contrib import admin
from .models import Student, Lesson, Tutor, TeachingRoom, Payment

# Register your models here.

admin.site.register(Payment)
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(Tutor)
admin.site.register(TeachingRoom)
