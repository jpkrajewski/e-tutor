from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from .models import Task, Lesson
from .forms import TaskForm
from .utils import FacebookMessengerAPI, NotificationHandler, RequestVerifier, LessonsUpdater
from django.conf import settings


@login_required
def home(request):
    print(settings.FACEBOOK_PAGE_VERIFY_TOKEN)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task(description=form.cleaned_data['description'], user_id=User.objects.get(id=1))
            task.save()
    form = TaskForm()
    usa = UserSocialAuth.objects.get(user_id=request.user.id)
    print(usa.user)
    return render(request=request,
                  template_name='index.html',
                  context={
                      'form': form,
                      'tasks': Task.objects.filter(user_id=1)
                  }
                  )


@login_required
def finish_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.is_done = True
        task.save()
    return redirect('home')


def login(request):
    return render(request, 'login.html')


@csrf_exempt
def facebook_messenger_webhook(request):
    if request.method == 'GET':
        return FacebookMessengerAPI.validate_webhook(request)

    if request.method == 'POST':
        return FacebookMessengerAPI.handle_post_request(request)


@csrf_exempt
def messenger_reminder(request):
    if request.method == 'POST':
        if RequestVerifier(request, settings.E_TUTOR_NOTIFICATION_TOKEN).verify():
            notification_handler = NotificationHandler(3, 1)
            if notification_handler.is_time_to_send_notification():
                notification_array = notification_handler.prepare_notification()
                for notification in notification_array:
                    FacebookMessengerAPI.call_send(**notification)
            return HttpResponse(200)
    return HttpResponse(403)


@csrf_exempt
def lessons_dates_update(request):
    if request.method == 'POST':
        if RequestVerifier(request, settings.E_TUTOR_UPDATE_LESSONS_TOKEN).verify():
            LessonsUpdater.update()
            return HttpResponse(200)
        return HttpResponse(403)


def teaching_room(request):
    return render(request, 'teaching-room.html')


def chat(request):
    return render(request, 'teaching-room.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

def test(request):
    return HttpResponse(Lesson.objects.incoming_lessons(2, 1))
