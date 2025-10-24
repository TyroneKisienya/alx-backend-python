from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'conversations/(?P<conversation_id>[^/.]+)/messages', MessageViewSet,basename='message')
url_pattern = [
    path("api/", include(router.urls))
]