# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chatroom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        input_message = text_data_json['message']
        user_message = text_data_json['user']
        

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': input_message,
                'user': user_message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        input_message = event['message']
        user_message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': input_message,
            'user':user_message
        }))