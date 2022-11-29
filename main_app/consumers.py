# chat/consumers.py
from calendar import c
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Chatroom, Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


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
        user_name = text_data_json['user']
        userid = text_data_json['userid']
        chatroom_id = text_data_json['roomid']

        await database_sync_to_async(Message.objects.create)(user_id_id=userid, username=user_name, chat_id_id=chatroom_id, message_body=input_message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': input_message,
                'user': user_name

            }

        )

    # Receive message from room group
    async def chat_message(self, event):
        input_message = event['message']
        user_message = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user': user_message,
            'message': input_message

        }))
