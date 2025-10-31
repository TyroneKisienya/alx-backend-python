from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AbstractUser, Message, MessageHistory, Notification
from .serializers import MessageSerializer, MessageHistoryserializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from .managers import UnreadMessagesManager

# Create your views here.
class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.filter(parent_message_isnull = True).select_related(
        'sender', 'recipient', 'parent_message').prefetch_related('history', 'replies',Prefetch(
            'replies__replies'
        ))
    serializer_class = MessageSerializer

    @action(detail=True, methods=['GET'])
    def history(self, request, pk=None):
        message =get_object_or_404(Message, pk=pk)
        history_records = message.history.all()

        serializer = MessageSerializer(history_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Accountdelete(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request ,*args, **kwargs):
        user = request.user
        user.delete()
        return Response(
            {'details: delete_user'}, status= status.HTTP_204_NO_CONTENT
        )
    
class InboxViewset(viewsets.ReadOnlyModelViewSet):
    serializer = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.all_messages(self.request.user)
    
    @action(detail=False, methods=['GET'])
    def unread(self, request):
        unread_messages = Message.unread.unread_for_user(request.user)
        serializer = self.get_serializer(unread_messages, many = True)
        return Response(serializer.data)