from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from .models import Lesson
from .utils import FacebookMessengerAPI, NotificationHandler, LessonsUpdater
from django.conf import settings


def home(request):
    return render(request, 'home.html')


@csrf_exempt
def facebook_messenger_webhook(request):
    if request.method == 'GET':
        return FacebookMessengerAPI.validate_webhook(request)

    if request.method == 'POST':
        return FacebookMessengerAPI.handle_post_request(request)


def lesson_room(request, room_name):

    if room_name != 'demo':
        return redirect('home')

    return render(request, 'lesson_room.html', {
        'room_name': room_name,
        'username': 'student'
    })

