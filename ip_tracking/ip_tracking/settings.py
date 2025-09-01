"""
Django settings for your project.
Add your project-specific settings below.
"""

INSTALLED_APPS = [
    # ...existing apps...
    'ip_tracking',
]

MIDDLEWARE = [
    # ...existing middleware...
    'ip_tracking.middleware.IPTrackingMiddleware',
]

# ...other settings...
