from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from .models import Lesson, Student, Tutor, TeachingRoom
from .forms import StudentCreateForm, LessonCreateForm
from .utils import FacebookMessengerAPI
from django.conf import settings
import requests
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


def home(request):
    return render(request, 'home.html')


@login_required
def profile_view(request):
    tutor_profile = request.user.tutor
    context = {'profile': tutor_profile}
    return render(request, 'profile.html', context=context)


class StudentCreateView(CreateView):
    template_name = 'student_create_form.html'
    form_class = StudentCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tutor = self.request.user.tutor
        self.object.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(StudentCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['tutor'] = self.request.user.tutor
        return kwargs


class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'


class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    # paginate_by = 100  # if pagination is desired


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


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson_detail.html'


class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson_list.html'
    # paginate_by = 100  # if pagination is desired


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

        student = teaching_room.lesson.student
        lesson = teaching_room.lesson

        return render(request, 'lesson_room.html', {
            'room_name': room_code,
            'username': 'student',
            'is_lesson_paid': True,
            'student': student,
            'lesson': lesson,
        })

    return redirect('home')

