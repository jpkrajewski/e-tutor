import requests
from django.conf import settings


class FacebookMessengerAPI:

    def get_verify_token(self):
        return settings.FACEBOOK_PAGE_VERIFY_TOKEN

    def call_send(self, senderPsid, response):
        page_access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
        payload = {
            'recipient': {'id': senderPsid},
            'message': response,
            'messaging_type': 'RESPONSE'
        }
        headers = {'content-type': 'application/json'}
        url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(page_access_token)
        r = requests.post(url, json=payload, headers=headers)
        print(r.text)

    # Function for handling a message from MESSENGER
    def handle_message(self, sender_psid, received_message):
        # check if received message contains text
        if 'text' in received_message:

            response = {"text": 'You just sent: {}'.format(received_message['text'])}

            self.call_send(sender_psid, response)
        else:
            response = {"text": 'This chatbot only accepts text messages'}
            self.call_send(sender_psid, response)
