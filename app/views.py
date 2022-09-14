from typing import Any, Dict
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Lesson, Payment, Student, Tutor, TeachingRoom
from .forms import StudentCreateForm, LessonCreateForm, StudentCreateFromCSVForm

from .utils import FacebookMessengerAPI
from .reports import get_money_per_week, get_students_missing_payments, get_total_student_missing_payment, get_lessons_today_and_tomorrow
from .calendar import order_lessons_from_this_week_by_days_and_hours, order_lessons_from_next_week_by_days_and_hours
from .library.etl_csv import etl_student_csv

def home(request):
    return render(request, 'home.html')


@login_required
def change_payment_status(request):
    payment = Payment.objects.get(pk=int(request.POST.get('id_payment')))
    payment.change_status_to_paid()
    payment.save()

    return redirect(request.POST.get('redirect_back_path'))


@method_decorator(login_required, name='dispatch')
class TutorProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        context = {
            'money_weekly': get_money_per_week(request.user.tutor.lesson_set.all()),
            'students_missing_payments': get_students_missing_payments(request.user.tutor.student_set.all()),
            'incoming_lessons_today_and_tomorrow': get_lessons_today_and_tomorrow(request.user.tutor.lesson_set),
        }

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class TutorReminderUpdateView(UpdateView):
    model = Tutor
    template_name = 'reminder.html'
    fields = ['send_reminder_hours_before',
              'send_reminders_to_yourself',
              'send_reminders_to_students',
              'message_template_to_yourself',
              'message_template_to_students']


@method_decorator(login_required, name='dispatch')
class StudentCreateView(CreateView):
    template_name = 'student_create_form.html'
    form_class = StudentCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(StudentCreateView, self).get_form_kwargs(
            *args, **kwargs)
        kwargs['tutor'] = self.request.user.tutor
        return kwargs


class StudentCreateFromCSVView(View):
    form_class = StudentCreateFromCSVForm
    template_name = 'student_create_from_csv_form.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():

            # TODO feedback
            feedback = etl_student_csv.etl(request.FILES['csv_with_students'], request.user.tutor)
            
            return redirect('students')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            lessons=self.object.lesson_set.all(),
            payments=self.object.payment_set.all(),
            total_missing_payment=get_total_student_missing_payment(
                self.object.payment_set),
        )


@method_decorator(login_required, name='dispatch')
class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'


@method_decorator(login_required, name='dispatch')
class LessonCreateView(CreateView):
    template_name = 'lesson_create_form.html'
    form_class = LessonCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LessonCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['tutor'] = self.request.user.tutor
        return kwargs


@method_decorator(login_required, name='dispatch')
class LessonUpdateView(UpdateView):
    template_name = 'lesson_create_form.html'
    form_class = LessonCreateForm
    model = Lesson

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LessonUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['tutor'] = self.request.user.tutor
        return kwargs


@method_decorator(login_required, name='dispatch')
class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson_detail.html'


@method_decorator(login_required, name='dispatch')
class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = object_list if object_list else self.object_list
        return super(LessonListView, self).get_context_data(
            object_list=object_list,
            lessons_this_week=order_lessons_from_this_week_by_days_and_hours(object_list),
            lessons_next_week=order_lessons_from_next_week_by_days_and_hours(object_list,)
        )


@csrf_exempt
def facebook_messenger_webhook(request):
    if request.method == 'GET':
        return FacebookMessengerAPI.validate_webhook(request)

    if request.method == 'POST':
        return FacebookMessengerAPI.handle_post_request(request)


def lesson_room(request, room_code):
    if room_code == 'demo':
        return render(request, 'lesson_room.html', {
            'room_name': room_code,
            'username': 'student',
            'is_lessons_paid': False,
        })

    teaching_room = TeachingRoom.objects.filter(url=room_code).first()
    if teaching_room:
        # from teaching room we can get all info we want to customize experience of a lesson
        # print(teaching_room.lesson.student.first_name)

        lesson = teaching_room.lesson

        if request.user.is_authenticated:
            username = request.user.username+'_tutor'
        else:
            username = lesson.student.first_name

        return render(request, 'lesson_room.html', {
            'room_name': room_code,
            'username': username,
            'lesson': lesson,
            'is_lesson_paid': True,
        })

    return redirect('home')
