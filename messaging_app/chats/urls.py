from .views import ConversationViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

message_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
message_router.register(r'messages', MessageViewSet,basename='conversation_messages')

urlpattern = [
    path('', include(routers.urls)),
    path('',include(message_router.urls)),
]