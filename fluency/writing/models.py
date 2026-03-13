from django.db import models
from django.conf import settings
from languages.models import Language

class WritingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    original_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SavedMistake(models.Model):
    writing_session = models.ForeignKey(WritingSession, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    incorrect_phrase = models.CharField(max_length=255)
    suggested_correction = models.CharField(max_length=255)
    error_message = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
# Create your models here.
