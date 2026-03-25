from django.db import models
from django.conf import settings

class SavedWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    turkish_meaning = models.CharField(max_length=150, blank=True, null=True) # 🔥 YENİ EKLENDİ
    language = models.CharField(max_length=5)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word} ({self.turkish_meaning}) - {self.user.username}"
