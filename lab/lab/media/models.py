from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Media(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name