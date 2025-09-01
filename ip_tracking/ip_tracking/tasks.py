
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db import models
from ip_tracking.models import RequestLog
from ip_tracking.ip_tracking.models import SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_anomalies():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)
    # Find IPs with >100 requests in the last hour
    ip_counts = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=models.Count('id'))
        .filter(count__gt=100)
    )
    for entry in ip_counts:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': 'More than 100 requests in the last hour'}
        )
    # Find IPs accessing sensitive paths
    for path in SENSITIVE_PATHS:
        logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__icontains=path)
        for log in logs:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                defaults={'reason': f'Accessed sensitive path: {path}'}
            )
