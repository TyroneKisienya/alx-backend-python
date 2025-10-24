from .views import ConversationsViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'conversations', ConversationsViewSet, basename='conversation')
router.register(r'conversations/(?P<conversation_id>[^/.]+)/messages', MessageViewSet,basename='message')
url_pattern = router.urls