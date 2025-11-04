import requests
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP


class RequestLoggingMiddleware:
    """
    Middleware to:
    1. Block requests from blacklisted IPs.
    2. Log IP, timestamp, and request path.
    3. Include geolocation data (country, city) using an external API.
    4. Cache geolocation results for 24 hours.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied: Your IP has been blocked.")

        # Get geolocation info (cached)
        geo_data = self.get_geolocation(ip)
        country = geo_data.get("country_name", "Unknown")
        city = geo_data.get("city", "Unknown")

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timezone.now(),
            path=request.path,
            country=country,
            city=city,
        )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP even when behind proxies."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_geolocation(self, ip):
        """Fetch geolocation from public API and cache for 24 hours."""
        if not ip:
            return {"country_name": "Unknown", "city": "Unknown"}

        cache_key = f"geo_{ip}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                geo_data = {
                    "country_name": data.get("country_name", "Unknown"),
                    "city": data.get("city", "Unknown"),
                }
                cache.set(cache_key, geo_data, 60 * 60 * 24)  # Cache 24 hours
                return geo_data
        except requests.RequestException:
            pass

        return {"country_name": "Unknown", "city": "Unknown"}
