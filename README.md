# ALX Backend Security: IP Tracking & Anomaly Detection

## Overview

This Django project implements advanced security features for backend systems, focusing on IP tracking, blacklisting, geolocation analytics, rate limiting, and anomaly detection. It is designed to help protect web applications from abuse, brute-force attacks, and suspicious activity.

## Features

- **IP Logging Middleware**: Logs every incoming request's IP address, timestamp, and path.
- **IP Blacklisting**: Blocks requests from blacklisted IPs and provides a management command to add IPs to the blacklist.
- **Geolocation Analytics**: Enhances logs with country and city information using the ipgeolocation API, with caching for efficiency.
- **Rate Limiting**: Limits requests per IP using `django-ratelimit` (10/min for authenticated, 5/min for anonymous users) on sensitive views.
- **Anomaly Detection**: Uses Celery to flag suspicious IPs that exceed 100 requests/hour or access sensitive paths (e.g., `/admin`, `/login`).

## Directory Structure

```bash
ip_tracking/
    ip_tracking/
        middleware.py         # Middleware for logging, blacklisting, geolocation
        models.py             # Models: RequestLog, BlockedIP, SuspiciousIP
        tasks.py              # Celery task for anomaly detection
        views.py              # Sensitive views (e.g., login) with rate limiting
        management/
            commands/
                block_ip.py   # Management command to add IPs to BlockedIP
    settings.py               # Django settings (add app, middleware, ratelimit config)
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kimoban/alx-backend-security.git
cd alx-backend-security
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# Or
source .venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# If requirements.txt is missing, install manually:
pip install django django-ratelimit ipgeolocation celery
```

### 4. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Configuration

- Add your `GEO_API_KEY` for the ipgeolocation API in `middleware.py` if required.
- Ensure `INSTALLED_APPS` and `MIDDLEWARE` in `settings.py` include the correct entries.

### 6. Running the Project

```bash
python manage.py runserver
```

### 7. Using the Management Command

Block an IP address:

```bash
python manage.py block_ip <ip_address>
```

### 8. Running Celery for Anomaly Detection

Start a Celery worker:

```bash
celery -A ip_tracking worker --beat --scheduler django --loglevel=info
```

## Models

- **RequestLog**: Stores IP, timestamp, path, country, city.
- **BlockedIP**: Stores blacklisted IPs.
- **SuspiciousIP**: Stores flagged IPs and reasons.

## Security Logic

- **Middleware**: Logs requests, blocks blacklisted IPs, enriches logs with geolocation.
- **Rate Limiting**: Applied to login view using `django-ratelimit`.
- **Anomaly Detection**: Celery task flags IPs with excessive requests or sensitive path access.

## Customization

- Adjust rate limits in `settings.py` as needed.
- Add more sensitive paths in `tasks.py` for anomaly detection.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Author

Isaiah Kimoban
