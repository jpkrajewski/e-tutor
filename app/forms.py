from django.forms import ModelForm
from .models import Student, Lesson


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class StudentForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ('tutor',)
