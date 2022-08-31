from datetime import datetime
from django import forms
from django.utils import timezone
from django.forms import ModelForm, DateTimeInput
from .models import Student, Lesson
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


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
        exclude = ('tutor', 'is_facebook_notification_send')

        widgets = {
            'start_datetime': DateTimeInput(format='%d/%m/%Y %H:%M:%S', attrs={'type': 'datetime-local'}),
            'end_datetime': DateTimeInput(format='%d/%m/%Y %H:%M:%S', attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop('tutor')
        super(LessonCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LessonCreateForm, self).clean()
        start_datetime = cleaned_data['start_datetime']
        end_datetime = cleaned_data['end_datetime']

        if end_datetime > start_datetime:
            raise forms.ValidationError('Lesson end date has to be later than start date')

        if start_datetime < datetime.now(tz=timezone.utc):
            raise forms.ValidationError("You can't make date later than now")

        return cleaned_data



