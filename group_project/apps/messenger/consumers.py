import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['room_name']
        self.receiver = await database_sync_to_async(User.objects.get)(id=self.receiver_id)
        self.room_group_name = f'chat_{self.scope["user"].id}_{self.receiver_id}'

        # 방 그룹에 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 방 그룹에서 제거
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']

        # 데이터베이스에 메시지 저장
        await database_sync_to_async(Message.objects.create)(
            sender=sender, receiver=self.receiver, content=message
        )
        
        # 방 그룹에 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # WebSocket을 통해 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))