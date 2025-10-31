from rest_framework import serializers
from .models import AbstractUser, Message, Notification, MessageHistory

class MessageHistoryserializer(serializers.ModelSerializer):
    class Meta:
        models = MessageHistory
        fields = ['old_content', 'edited_at', 'edited_by']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        models  = Notification
        fields  =['message', 'content']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        models = Message
        fields = ['sender', 'content', 'timestamp']
