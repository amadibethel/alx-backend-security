# ip_tracking/middleware.py
from django.utils import timezone
from .models import RequestLog

class RequestLoggingMiddleware:
    """
    Middleware to log IP address, timestamp, and path of each incoming request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract client IP
        ip = self.get_client_ip(request)

        # Log request details
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timezone.now(),
            path=request.path
        )

        # Continue to the next middleware/view
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP, considering possible proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

