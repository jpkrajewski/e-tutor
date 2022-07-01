from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from .models import Task
from .forms import TaskForm
from .utils import FacebookMessengerAPI as FBMessenger
import json
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


def facebook_messenger_webhook(request):
    if request.method == 'GET':
        return FBMessenger.validate_webhook(request)

    if request.method == 'POST':
        return FBMessenger.handle_post_request(request)
