from django.db import models
class UnreadMessagesManager(models.Manager):
    def unread_messages(self, user):
        return self.filter(recipient = user, unread = False).only('id', \
        'sender', 'content','timestamp', 'unread'). select_related('sender')
    
    def all_messages(self, user):
        return self.filter(recipient = user).only('id','sender', 'content', 'timestamp'
                                                  ,'unread').select_related('sender')