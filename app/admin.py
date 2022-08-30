from django.contrib import admin
from .models import Student, Lesson, FacebookMessage, Tutor, TeachingRoom

# Register your models here.

admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(Tutor)
admin.site.register(FacebookMessage)
admin.site.register(TeachingRoom)
