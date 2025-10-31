from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import AbstractUser

@receiver(post_save, sender = Message)
def notify(sender, instance, created, **kwargs):
    if created:
        recipient_user = instance.recipient
        sender_user = instance.sender
        content = f'New message from {sender_user.username}: {instance.content[:40]}'
        Notification.objects.create(
            recipient = recipient_user,
            message = instance,
            content = content
        )
        print(f'Notification for {recipient_user.username}')

@receiver(pre_save, sender = Message)
def sms_history(sender,instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Message.objects.get(pk = instance.pk)
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message = instance,
                    old_content = old_instance.content
                )
                instance.edited = True
                print(f'Message hostory {instance.pk}')
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender = AbstractUser)
def cleanup(sender, instance, **kwargs):
    user_id = instance.id
    username = instance.username

    print(f'Deleted: {username} (ID: {id} starting cleanup)')
    deleted_notify, notify_details = Notification.objects.filter(
        recipient = instance).delete()
    print(f'deleted {deleted_notify}')
    print(f'data cleanup for {username}')