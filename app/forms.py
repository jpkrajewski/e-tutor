from django import forms
from django.forms import ModelForm
from .models import Student, Lesson


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        exclude = ('tutor',)

    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop('tutor')
        super(StudentCreateForm, self).__init__(*args, **kwargs)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Student.objects.filter(tutor=self.tutor, phone_number=phone_number).exists():
            raise forms.ValidationError('You have already a student with same phone number')
        return phone_number


class LessonCreateForm(ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'


