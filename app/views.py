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
        verify_token = FBMessenger.get_verify_token()
        if request.GET["hub.mode"] == "subscribe" and request.GET["hub.challenge"]:
            if not request.GET["hub.verify_token"] == verify_token:
                return HttpResponse("Verification token missmatch", 403)
            return HttpResponse(request=request.GET['hub.challenge'], status=200)
        return HttpResponse("Hello world", 200)

    if request.method == 'POST':
        #do something.....
        VERIFY_TOKEN = FBMessenger.get_verify_token()

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        #do something else
        data = request.data
        body = json.loads(data.decode('utf-8'))

        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))

                if 'message' in webhookEvent:
                    FBMessenger.handle_message(senderPsid, webhookEvent['message'])

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404
