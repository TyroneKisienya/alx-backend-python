from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AbstractUser, Message, MessageHistory, Notification
from .serializers import MessageSerializer, MessageHistoryserializer, NotificationSerializer

# Create your views here.
class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer

    @action(detail=True, methods=['GET'])
    def history(self, request, pk=None):
        message =get_object_or_404(Message, pk=pk)
        history_records = message.history.all()

        serializer = MessageSerializer(history_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)