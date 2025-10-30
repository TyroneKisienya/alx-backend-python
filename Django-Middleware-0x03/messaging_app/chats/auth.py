from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import exceptions

class JWT_Sess_AUTh(JWTAuthentication):
    def authenticate(self, request):
        user_auth = super().authenticate(request)
        if user_auth:
            return user_auth
        
        try:
            sess_auth = SessionAuthentication().authenticate(request)
            if sess_auth:
                return sess_auth
        except exceptions:
            pass
        return None