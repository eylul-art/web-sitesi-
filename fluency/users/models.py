from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser # Bunu ekle

# 1. Eksik olan User modelini buraya tanımlıyoruz
class User(AbstractUser):
    pass

# 2. Senin yazdığın seviye modeli (Burası aynen kalabilir)
class UserLanguageLevel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    language_code = models.CharField(max_length=5)
    level = models.CharField(max_length=2, default='A1')
    last_tested = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.language_code} - {self.level}"