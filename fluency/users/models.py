from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Şemadaki özel alanlar
    email = models.EmailField(unique=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Şemadaki target language ve level ilişkileri (opsiyonel ama şemada var)
    target_language_id = models.IntegerField(null=True, blank=True)
    target_level_id = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
# Create your models here.
