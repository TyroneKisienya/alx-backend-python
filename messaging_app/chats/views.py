from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import Messageserializer, Conversationserializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class ConversationViewSet(viewsets.ViewSet):
    query_set = Conversation.objects.all()
    serializer_class = Conversationserializer

    @action(detail=True, methods=['post'], url_path='send_message')
    def send_message(self, request, pk=None):
        Conversation = self.get_object()

        serializer = Messageserializer(data=request.data)

        if serializer.is_valid():
            serializer.save(Conversation.conversation, sender=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MessageViewSet(viewsets.ViewSet):
    query_set = Message.objects.all()
    serializer_class = Messageserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filters(Conversation__id = self.request.user)
