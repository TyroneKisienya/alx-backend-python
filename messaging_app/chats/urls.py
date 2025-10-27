from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

message_router = routers.NestedDefaultRouter(router,r'conversations', lookup='conversation')
message_router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(message_router.urls))
]