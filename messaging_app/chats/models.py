from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length = 250)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(null=False, max_length=128)
    phone_number = models.CharField(max_length=250)
    class roleType(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'ADMIN'

    role = models.CharField(choices=roleType.choices, max_length=128, null= False)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(max_length=250)
    sent_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    participants_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
