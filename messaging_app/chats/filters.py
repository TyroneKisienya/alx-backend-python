import django_filters
from .models import User, Message
from messaging_app.chats import models

class MessageFilter(django_filters.filterset):

    username = django_filters.CharFilter(
        method= 'filter_by_conversation_user'
        label= 'Filter by a specific user\s username'
    )
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['username', 'created_at']
    
    def filter_by_conversation_user(self, queryset, name, value):
        try:
            conversation_user = User.objects.get(username = value)
            return queryset.filter(
                models.Q(sender=self.request.user, receiver=conversation_user) |
                models.Q(sender=conversation_user, receiver = self.request.user)
            )
        except User.DoesNotExist:
            return queryset.none()