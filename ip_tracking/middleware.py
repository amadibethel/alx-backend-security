# ip_tracking/middleware.py
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP


class RequestLoggingMiddleware:
    """
    Middleware that:
    1. Blocks blacklisted IPs (403 Forbidden).
    2. Logs all other requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Check blacklist
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied: Your IP has been blocked.")

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timezone.now(),
            path=request.path
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract the real client IP, even behind proxies."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
