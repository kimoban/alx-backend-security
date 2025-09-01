from django.db import models

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"
