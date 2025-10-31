from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(AbstractUser,default=uuid.uuid4, related_name='sent_messages')
    receiver = models.ForeignKey(AbstractUser, default=uuid.uuid4, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)

class Notification(models.Model):
    recipient = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=128)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)