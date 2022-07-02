import requests
from django.conf import settings
from django.http import HttpResponse
from .models import FacebookMessage
import json


class FacebookMessengerAPI:
    """
    Class used to handle everything related to Facebook Messanger API
    """

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
        page_access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
        payload = {
            'recipient': {'id': sender_psid},
            'message': message,
            'messaging_type': 'MESSAGE_TAG'
        }
        headers = {'content-type': 'application/json'}
        url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(page_access_token)
        requests.post(url, json=payload, headers=headers)

    @classmethod
    def handle_post_request(cls, request):
        new_msg = FacebookMessage(message='',
                                  sender_psid='',
                                  request_data=json.loads(request.body))
        new_msg.save()
        return HttpResponse('OK', 200)
