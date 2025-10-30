import logging
from datetime import datetime

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
        log_entry = (
            'f"{datetime.now()} - User: {user} - Path: {request.path}“'
        )
        self.logger.info(log_entry)

        response = self.get_response(request)

        return response