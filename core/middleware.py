# core/middleware.py

from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class CSRFMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.COOKIES.get('csrftoken'):
            csrf_token = get_token(request)
            response.set_cookie('csrftoken', csrf_token)
            logger.debug(f"CSRF token generated and set in cookie: {csrf_token}")
        return response