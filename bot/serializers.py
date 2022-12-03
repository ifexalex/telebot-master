from rest_framework import serializers
from account.models import TelegramUser, TelegramUserMessage


class BotSerializer(serializers.ModelSerializer):
    """
    Serializer for Bot model
    """


    class Meta:
        model = TelegramUser
        fields = "__all__"


class ClearChatSerializer(serializers.Serializer):
    """
    Serializer for Bot model
    """
    chat_id = serializers.IntegerField()


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Bot model
    """

    class Meta:
        model = TelegramUserMessage
        fields = "__all__"