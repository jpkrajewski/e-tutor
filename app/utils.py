import requests
from django.conf import settings
from django.http import HttpResponse
from .models import FacebookMessage, Lesson
import json
from datetime import datetime, timedelta


class FacebookMessengerAPI:
    """Class used to handle everything related to Facebook Messanger API"""

    @classmethod
    def validate_webhook(cls, request):
        """
        We verify if GET request has valid verifying token. Only Facebook has good token.
        Then if we confirm that the facebook is sending request we return challenge from
        request because they want it back.

        :param request: HTTP request
        :return: HTTP response
        """
        if not request.GET["hub.verify_token"] == settings.FACEBOOK_PAGE_VERIFY_TOKEN:
            return HttpResponse(403)
        return HttpResponse(request.GET['hub.challenge'], 200)

    @classmethod
    def call_send(cls, sender_psid, message):
        """
        Sending customized message to client.

        :param sender_psid: str
        :param message: str
        :return: HTTP response status code: int
        """

        page_access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
        payload = {
            "messaging_type": "MESSAGE_TAG",
            "recipient": {"id": sender_psid},
            "message": {"text": message}
        }
        headers = {'content-type': 'application/json'}
        url = 'https://graph.facebook.com/v14.0/me/messages?access_token={}'.format(page_access_token)
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    @classmethod
    def handle_post_request(cls, request):
        """
        Store message form client to your page. Save client first and last name,
        so you can bind it to automatic messages to inform about something.

        :param request: POST request
        :return: HTTP response to Facebook
        """

        post_request = json.loads(request.body)
        sender_psid = post_request['entry'][0]['messaging'][0]['sender']['id']
        sender_message = post_request['entry'][0]['messaging'][0]['message']['text']

        client_data = cls._get_client_data(sender_psid, 'name', 'gender', 'locale', 'timezone')
        new_msg = FacebookMessage(full_name=client_data,
                                  message=sender_message,
                                  sender_psid=sender_psid,
                                  request_data=post_request)
        new_msg.save()

        message_back = """
        Dziękuje za wiadomość, odpiszę jak najszybciej:)
        imie: {0}
        plec: {1}
        locale: {2}
        timezone: {3}
        """.format(client_data['name'],
                   client_data['gender'],
                   client_data['locale'],
                   client_data['timezone'])

        cls.call_send(sender_psid, message_back)
        return HttpResponse('OK', 200)

    @classmethod
    def _get_client_data(cls, sender_psid, *args):
        """
        Get client data by sender_id. Choose what data you want by including those fields as string.
        Available fields:
        'name','first_name','last_name','profile_pic','locale','timezone','gender'

        :param sender_psid: str
        :param kwargs:
        :return:
        """

        fields = ','.join(list(map(str, args)))
        url = f"https://graph.facebook.com/{sender_psid}?" \
              f"fields={fields}&" \
              f"access_token={settings.FACEBOOK_PAGE_ACCESS_TOKEN}"

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(response['error']['message'])
        return response.json()


class RequestVerifier:

    def __init__(self, request, token):
        self.request = request
        self.token = token

    def verify(self):
        if self.request.POST.get('e-tutor-token') == self.token:
            return True
        return False


class NotificationHandler:

    def __init__(self, tutor_id, hours_before):
        self.tutor_id = tutor_id
        self.hours_before = hours_before
        self.tutor_incoming_lessons = None

    def is_time_to_send_notification(self):
        self.tutor_incoming_lessons = Lesson.objects.incoming_lessons(self.hours_before, 1)
        if not self.tutor_incoming_lessons:
            return False
        return True

    # TODO: create profiles where tutors can add their own template to send to clients
    def prepare_notification(self) -> list:
        """
        :return: array with dict pair id:client_id, message:message to sent  to send
        """

        message_template_tutor = 'Hey, masz o {0} zajęcia z {1}'
        message_template_student = NotImplemented

        notification_array = []
        for lesson in self.tutor_incoming_lessons:
            # every incoming lesson by tutors gets taken and send to clients
            notification_array.append({'sender_psid': 5458874970818405,
                                       'message': message_template_tutor.format(lesson.lesson_start_datetime,
                                                                                lesson.student_id.name)
                                       })

        return notification_array


class LessonsUpdater:

    @classmethod
    def update(cls):
        done_lessons = Lesson.objects.get_done_lessons()

        if not done_lessons:
            return

        try:
            for lesson in done_lessons:
                lesson.lesson_start_datetime += timedelta(days=7)
                lesson.lesson_end_datetime += timedelta(days=7)
                lesson.save()

        except Exception as e:
            print(e)
