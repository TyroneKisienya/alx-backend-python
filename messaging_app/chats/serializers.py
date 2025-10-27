from rest_framework import serializers
from .models import User, Message, Conversation

class Userserializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
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
        def get_name(self, obj):
            return f'{obj.first_name} {obj.last_name}'.strip()
        def validate_email(self, value):
            if 'ban' in value:
                raise serializers.ValidationError('The Email is not allowed')
            return value

class Messageserializer(serializers.ModelSerializer):
    sender_id = Userserializer(read_only=True)
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
    messages = Messageserializer(many=True, read_only=True)
    participant_id = Userserializer(many=True, read_only=True)
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
