import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden

def logger():
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('request_log.log')
    formatter = logging.Formatter('%(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logger()

    def __call__(self, request):
        user = request.user
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}“
        self.logger.info(log_entry)

        response = self.get_response(request)

        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.forbid_start = time(21, 0)
        self.forbid_end  = time(6,0)

    def __call__(self,request):
        now = datetime.now().time()

        if (self.forbid_start <= now) or (now < self.forbid_end):
            return HttpResponseForbidden('Restricted Access')
        response = self.get_response(request)
        return response