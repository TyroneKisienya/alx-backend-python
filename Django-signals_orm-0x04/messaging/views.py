from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AbstractUser, Message, MessageHistory, Notification
from .serializers import MessageSerializer, MessageHistoryserializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

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
        sender = request.user

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