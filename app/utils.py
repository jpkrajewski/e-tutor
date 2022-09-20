import requests
from django.conf import settings
from django.http import HttpResponse
from .models import Lesson
import json
from datetime import datetime, timedelta
from django.conf import settings


class FacebookMessengerAPI:
    """Class used to handle everything related to Facebook Messanger API"""

    @classmethod
    def validate_webhook(cls, request):
        """
        We verify if GET request has valid verifying token. Only Facebook has good token.
        Then if we confirm that the facebook is sending request we return challenge from
        request because they want it back.

        :param request: HTTP request from facebook with verification token in params
        :return: HTTP response
        """

        if not request.GET["hub.verify_token"] == settings.FACEBOOK_PAGE_VERIFY_TOKEN:
            return HttpResponse(403)
        return HttpResponse(request.GET['hub.challenge'], 200)

    @classmethod
    def call_send(cls, payload):
        """
        Sending customized message to client.

        :param sender_psid: str
        :param message: str
        :return: HTTP response status code: int
        """

        page_access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN

        headers = {'content-type': 'application/json'}
        url = 'https://graph.facebook.com/v14.0/me/messages?access_token={}'.format(
            page_access_token)
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

        client_data = cls._get_client_data(
            sender_psid, 'name', 'gender', 'locale', 'timezone')
        new_msg = dict(
            full_name=client_data,
            message=sender_message,
            sender_psid=sender_psid,
            request_data=post_request
        )
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


class Reminder:
    """Class to create message"""

    def __init__(self, template: str, lesson: Lesson):
        self._message = template.format(
            start=lesson.start_datetime.astimezone().strftime("%m/%d/%Y, %H:%M"),
            end=lesson.end_datetime.astimezone().strftime("%m/%d/%Y, %H:%M"),
            sfname=lesson.student.first_name,
            slname=lesson.student.last_name,
            description=lesson.description,
            place=lesson.place,
            subject=lesson.subject,
            address=lesson.student.address,
        )

        if lesson.place == Lesson.ONLINE:
            self._message += f'\n\nLink do zajęć online: {lesson.teachingroom.get_absolute_url()}'

    def get_content(self):
        return self._message


class ReminderFacebookWrapper:
    """Wrapper for reminder to fit into Facebook API requirements"""

    def __init__(self, psid, message):
        self._message = {
            "messaging_type": "MESSAGE_TAG",
            "recipient": {"id": psid},
            "message": {"text": message}
        }

    def get_message(self):
        return self._message





