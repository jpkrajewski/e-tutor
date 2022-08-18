from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from .models import Lesson
from .utils import FacebookMessengerAPI, NotificationHandler, LessonsUpdater
from django.conf import settings
import requests


def home(request):
    return render(request, 'home.html')



def profile(request):
    payload = {
        "messaging_type": "MESSAGE_TAG",
        "recipient": {"id": 5458874970818405},
        "message": {"text": 'test'}
    }

    headers = {'content-type': 'application/json'}
    url = 'https://graph.facebook.com/v14.0/me/messages?access_token={}'.format('EAAIE42HZBvzkBAByZBluiDXuHvpk7UkwyZBDZCKckGDXMjFMlE83D9D6LbKJ7ucChId12GsxFLBYuaC9Xs0KG7iI7xX4KXGEa14ejjbx32yUwt51DEUJkXTdSBHVtC9JNtzghU9IhSEWU7sgT2gmkS2qItRd4OVbbfAt4QEYUdyqeECEGm8b')
    response = requests.post(url, json=payload, headers=headers)



    return render(request, 'profile.html')


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

