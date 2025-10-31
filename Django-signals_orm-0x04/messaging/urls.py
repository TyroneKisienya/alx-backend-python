from rest_framework.routers import DefaultRouter
from .views import MessageViewset, Accountdelete
from django.urls import path, include


router = DefaultRouter
router.register(r'message', MessageViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('',Accountdelete.as_view(), name= 'account_delete')
]