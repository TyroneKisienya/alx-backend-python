import logging
from datetime import datetime, time, timedelta
from requests import request
from django.http import HttpResponseForbidden
from django.core.cache import cache

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
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5
        self.window_min = 1
        self.logger = logging.getLogger(__name__)

    def get_ip():
        x_forwared_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwared_for:
            ip = x_forwared_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith(''):
            ip = self.get_ip(request)
            cache_key = f'rate_limit {ip}'

            timestamps = cache.get(cache_key, [])

            time_window = datetime.now() - timedelta(minutes = self.window_min)
            timestamps = [ts for ts in timestamps if ts > time_window]
            
            if len(timestamps) >= self.limit:
                self.logger.warning(f'Rate limit exceeded {ip}')
                return HttpResponseForbidden('You have sent too many messages')
            
            timestamps.append(datetime.now())
            cache.set(cache_key, timestamps, self.window_min * 60)

        response = self.get_response(request)
        return response