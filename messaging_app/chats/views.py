from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import Messageserializer, Conversationserializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
from .permissions import IsParticipantofConversation

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = Conversationserializer
    permission_classes = [IsAuthenticated, IsParticipantofConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants_id=self.request.user)

    @action(detail=True, methods=['post'], url_path='send_message')
    def send_message(self, request, pk=None):
        Conversation = self.get_object()

        self.check_object_permissions(request, Conversation)

        serializer = Messageserializer(data=request.data)

        if serializer.is_valid():
            serializer.save(Conversation.conversation, sender_id=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = Messageserializer
    permission_classes = [IsAuthenticated, IsParticipantofConversation]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filters(Conversation__participants_id = user)
    
    def perform_create(self, serializer):
        raise NotImplementedError('use the "send_message" to send a message')
