import requests
from django.conf import settings


class FacebookMessengerAPI:

    @classmethod
    def get_verify_token(cls):
        return settings.FACEBOOK_PAGE_VERIFY_TOKEN

    @classmethod
    def call_send(cls, sender_psid, response):
        page_access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
        payload = {
            'recipient': {'id': sender_psid},
            'message': response,
            'messaging_type': 'RESPONSE'
        }
        headers = {'content-type': 'application/json'}
        url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(page_access_token)
        r = requests.post(url, json=payload, headers=headers)
        print(r.text)

    @classmethod
    def handle_message(cls, sender_psid, received_message):
        # check if received message contains text
        if 'text' in received_message:

            response = {"text": 'You just sent: {}'.format(received_message['text'])}

            cls.call_send(sender_psid, response)
        else:
            response = {"text": 'This chatbot only accepts text messages'}
            cls.call_send(sender_psid, response)
