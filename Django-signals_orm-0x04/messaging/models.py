from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from .managers import UnreadMessagesManager

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(AbstractUser,default=uuid.uuid4, related_name='sent_messages')
    receiver = models.ForeignKey(AbstractUser, default=uuid.uuid4, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    edited = models.BooleanField(default=False)
    unread = models.BooleanField(default=False)
    objects = UnreadMessagesManager()
    parent_message = models.ForeignKey(
        'self',
        null = False,
        on_delete=models.set_Null,
        related_name='replies'
    )
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'message: {self.id} (edited: {self.edited})'
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.CharField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='username')
    class Meta:
        ordering = ['-edited_at']
        verbose_plural_name = 'Message_History'

        def __str__(self):
            return f'message: {self.id} at {self.edited_at.strftime('%Y-%m-%d %H-%m')}'
class Notification(models.Model):
    recipient = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=128)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)