from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from ip_tracking.models import RequestLog, SuspiciousIP


@shared_task
def detect_anomalies():
    """
    Runs hourly to flag suspicious IPs that:
    1. Make more than 100 requests/hour.
    2. Access sensitive paths like /admin or /login.
    """

    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Rule 1: High-frequency requests (>100/hour)
    ip_counts = {}
    for log in recent_logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f'High request volume: {count} requests/hour'},
            )

    # Rule 2: Accessing sensitive paths
    sensitive_paths = ['/admin', '/login', '/settings', '/config']
    for log in recent_logs:
        if any(log.path.startswith(p) for p in sensitive_paths):
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                defaults={'reason': f'Accessed sensitive path: {log.path}'},
            )

    return "Anomaly detection completed."

