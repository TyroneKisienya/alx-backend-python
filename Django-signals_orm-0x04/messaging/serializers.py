from rest_framework import serializers
from .models import AbstractUser, Message, Notification, MessageHistory

class MessageHistoryserializer(serializers.ModelSerializer):
    class Meta:
        models = MessageHistory
        fields = ['old_content', 'edited_at', 'edited_by']

