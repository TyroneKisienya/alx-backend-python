from requests import request
from rest_framework import permissions

class IsParticipantofConversation(permissions.BasePermission):
    message = 'You must be logged in'

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(obj,'participants_id'):
            is_participant = obj.participants_id.filter(user_id = request.user.user_id).exists()
        elif hasattr(obj, 'conversation'):
            is_participant = obj.conversation.participants_id.filter(user_id = request.user.user_id).exists()
        else:
            return False
        return is_participant