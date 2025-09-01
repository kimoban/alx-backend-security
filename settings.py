
# Application definition
INSTALLED_APPS = [
	'ip_tracking',
	'ratelimit',
]

# Middleware definition
MIDDLEWARE = [
	'ip_tracking.middleware.IPTrackingMiddleware',
]

# django-ratelimit settings
RATELIMIT_ENABLE = True
RATELIMIT_VIEW = 'ip_tracking.views.login_view'
RATELIMIT_RATE = '10/m'
RATELIMIT_ANONYMOUS_RATE = '5/m'
