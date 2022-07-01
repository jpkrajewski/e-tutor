from django.forms import ModelForm
from .models import Task, Student


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'