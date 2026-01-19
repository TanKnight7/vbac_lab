from django.db import models

class Plugin(models.Model):
    name = models.CharField(max_length=150)
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.version})"
