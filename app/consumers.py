# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DrawConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'lesson_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        print(text_data)

        text_data_json = json.loads(text_data)

        if not text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {})

        message = text_data_json['message']

        data_dict = None
        match message:
            case 'clear':
                data_dict = {
                    'type': 'clear_message',
                    'message': message,
                }

            case 'down':
                data_dict = {
                    'type': 'draw_message',
                    'message': text_data_json
                }

            case 'move':
                data_dict = {
                    'type': 'draw_message',
                    'message': text_data_json
                }

            case {}:
                data_dict = {
                    'type': 'draw_message',
                    'message': text_data_json
                }


        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, data_dict)

    def clear_message(self, event):
        message = event['message']
        print(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # Receive message from room group
    def draw_message(self, event):
        message = event['message']
        print(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
