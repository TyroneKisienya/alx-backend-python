from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import Messageserializer, Conversationserializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
from .permissions import IsParticipantofConversation
from rest_framework import status
from .pagination import NumberPagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from messaging_app.chats import models
from django.utils.decorators import method_decorator

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
    pagination_class = NumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        self.check_object_permissions(self.request, conversation)
        return Message.objects.filter(conversation=conversation | models.Q(sender = self.request.user | models.Q(receiver = self.request.user)))
    
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=  True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        self.check_object_permissions(self.request, conversation)
        serializer.save(sender_id=self.request.user, conversation=conversation)
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)