from datetime import datetime
from typing import Any, Dict, Optional

from django import forms
from django.utils import timezone
from django.forms import DateTimeInput, Textarea
from .models import Student, Lesson, Tutor


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('tutor',)

    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop('tutor')
        super(StudentCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(StudentCreateForm, self).clean()
        if (Student.objects.filter(tutor=self.tutor, phone_number=cleaned_data['phone_number']).exists()
                and self.cleaned_data['phone_number']):
            raise forms.ValidationError(
                'Student with same the phone number already exists')

        if (Student.objects.filter(tutor=self.tutor, discord_nick=cleaned_data['discord_nick']).exists()
                and self.cleaned_data['discord_nick']):
            raise forms.ValidationError(
                'Student with same the discord nick already exists')

        if (Student.objects.filter(tutor=self.tutor, email=cleaned_data['email']).exists()
                and self.cleaned_data['email']):
            raise forms.ValidationError(
                'Student with same the email already exists')

        return cleaned_data


class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ('tutor', 'is_notification_send', )

        widgets = {
            'start_datetime': DateTimeInput(format='%d/%m/%Y %H:%M:%S', attrs={'type': 'datetime-local'}),
            'end_datetime': DateTimeInput(format='%d/%m/%Y %H:%M:%S', attrs={'type': 'datetime-local'}),
            'description': Textarea(),
        }

    def __init__(self, *args, **kwargs):
        self.tutor = kwargs.pop('tutor')
        super(LessonCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LessonCreateForm, self).clean()
        start_datetime = cleaned_data['start_datetime']
        end_datetime = cleaned_data['end_datetime']

        if end_datetime < start_datetime:
            raise forms.ValidationError(
                'Lesson end date has to be later than start date')

        if start_datetime < datetime.now(tz=timezone.utc):
            raise forms.ValidationError("You can't make date later than now")

        return cleaned_data


class StudentCreateFromCSVForm(forms.Form):
    csv_with_students = forms.FileField(widget=forms.widgets.FileInput(attrs={'accept': '.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'}))
