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
        #sender_psid = post_request['entry'][0]['messaging'][0]['sender']['id']
        #sender_message = post_request['entry'][0]['messaging'][0]['message']['text']

        #url = f"https://graph.facebook.com/{sender_psid}?fields=name,first_name,last_name,profile_pic,locale,timezone,gender&access_token={settings.FACEBOOK_PAGE_ACCESS_TOKEN}"
        #res = requests.get(url)
        #res = res.json()

        # new_msg = FacebookMessage(full_name=res['name'],
        #                           message=sender_message,
        #                           sender_psid=sender_psid,
        #                           request_data=post_request)
        # new_msg.save()

        new_msg = FacebookMessage(full_name='1', message='1', sender_psid='1', request=post_request)
        new_msg.save()


        # mess_back = """Dziękuje za wiadomość, odpiszę jak najszybciej:)
        # imie: {0}
        # plec: {1}
        # locale: {2}
        # timezone: {3}
        # """.format(res['name'], res['gender'], res['locale'], res['timezone'])
        #
        # cls.call_send(sender_psid, mess_back)
        return HttpResponse('OK', 200)

    def _get_client_data(self, sender_psid, **kwargs):
        """
        Get client data by sender_id. Choose what data you want by specifying fields.
        Available fields:

        'name'
        The user's first and last name

        'first_name'
        First name

        'last_name'
        Last name

        'profile_pic'
        URL to the Profile picture. The URL will expire.

        'locale'
        Locale of the user on Facebook. For supported locale codes, see Supported Locales.

        'timezone'
        Timezone, number relative to GMT

        'gender'
        Gender

        :param sender_psid: str
        :param kwargs:
        :return:
        """
        pass
