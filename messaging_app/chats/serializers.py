from rest_framework import serializers
from .models import User, Message, Conversation

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'first_name',
            'last_name',
            'email',
            'role',
            'created_at'
        )
        read_only_fields = (
            'user_id',
            'role',
            'created_at',
            )
        extra_kwargs = {
            'role': {'default': User.roleType.GUEST
            }
        }

class Messageserializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'message_id',
            'sender_id',
            'message_body',
            'sent_at'
        )
        read_only_fields = (
            'message_body',
            'sent_at',
        )

class Conversationserializer(serializers.ModelSerializer):
    messages = Messageserializer(many=True)
    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participant_id',
            'created_at'
        )
        read_only_fields = (
            'conversation_id',
            'participant_id',
            'created_at',
        )