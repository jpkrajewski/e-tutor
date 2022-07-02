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
        """

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
        return response.status_code

    @classmethod
    def handle_post_request(cls, request):
        """
        XDDDDDDDD

        :param request: POST request
        :return: HTTP response
        """
        post_request = json.loads(request.body)
        sender = post_request['entry'][0]['messaging'][0]['sender']['id']
        new_msg = FacebookMessage(message=post_request['entry'][0]['messaging'][0]['message']['text'],
                                  sender_psid=sender,
                                  request_data=json.loads(request.body))
        new_msg.save()
        cls.call_send(sender, 'ELO KURWA')
        return HttpResponse('OK', 200)
