from email.message import Message
from django.shortcuts import render
from rest_framework.response import Response
import telegram
from .serializers import BotSerializer, ClearChatSerializer, MessageSerializer
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async, async_to_sync
from rest_framework.parsers import JSONParser
from functools import wraps
from account.models import TelegramUser
import asyncio
from django.db.transaction import atomic


def to_async(blocking):
    @wraps(blocking)
    def run_wrapper(*args, **kwargs):
        return asyncio.run(blocking(*args, **kwargs))

    return run_wrapper

    


class DeleteChatHistoryView(viewsets.ModelViewSet):
    """
    ViewSet for deleting chat history
    """
    serializer_class = MessageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Deletes chat history
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = TelegramUser.objects.get(id = serializer.validated_data['telegram_user'].id)
        with atomic():
            user.clear_chat()
            user.delete()
        return Response(
            {
                "message": "User account and chat history deleted"
            },
            status=status.HTTP_200_OK
        )

    
class SendMessageView(viewsets.ModelViewSet):
    """
    ViewSet for sending message
    """
    serializer_class = MessageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Sends message
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = TelegramUser.objects.get(id = serializer.validated_data['telegram_user'].id)
        
        message = user.send_message(serializer.validated_data['message'])
        TelegramUser.append_message_id(user.chat_id, message.message_id)
        return Response(
            {
                "message": f"Message sent to {user.username}"

            },
            status=status.HTTP_200_OK
        )
