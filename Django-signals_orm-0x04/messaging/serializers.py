from rest_framework import serializers
from .models import AbstractUser, Message, Notification, MessageHistory

class RecursiveMessageSerializer(serializers.ModelSerializer):
    def to(self, value):
        serializer = MessageSerializer(value, context= self.context)
        return serializer.data
class MessageHistoryserializer(serializers.ModelSerializer):
    class Meta:
        models = MessageHistory
        fields = ['old_content', 'edited_at', 'edited_by']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        models  = Notification
        fields  =['message', 'content']

class MessageSerializer(serializers.ModelSerializer):
    sender = AbstractUser(read_only = True)
    receiver = AbstractUser(read_only = True)
    history = MessageHistory(many= True, read_only= True)
    replies = RecursiveMessageSerializer(many = True, read_only = True)
    class Meta:
        models = Message
        fields = ['sender', 'content', 'timestamp', 'receiver', 'parent_message', 'edited']
        read_only_fields = ['content', 'timestamp', 'parent_message', 'receiver']

        def create(self, validated_data):
            return Message.objects.create(**validated_data)