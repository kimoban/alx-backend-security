



from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.cache import cache

from ipgeolocation import IpGeolocationAPI

from .models import RequestLog, BlockedIP

GEO_API_KEY = None  # Set your API key if required
geo = IpGeolocationAPI(api_key=GEO_API_KEY)

class IPTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        # Block if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden('Your IP is blacklisted.')
        path = request.path
        timestamp = timezone.now()

        # Geolocation caching for 24 hours
        cache_key = f'geo_{ip}'
        geo_data = cache.get(cache_key)
        if not geo_data:
            try:
                response = geo.get_geolocation(ip_address=ip)
                geo_data = {
                    'country': response.get('country_name', ''),
                    'city': response.get('city', '')
                }
            except Exception:
                geo_data = {'country': '', 'city': ''}
            cache.set(cache_key, geo_data, 60 * 60 * 24)  # 24 hours

        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timestamp,
            path=path,
            country=geo_data.get('country', ''),
            city=geo_data.get('city', '')
        )
