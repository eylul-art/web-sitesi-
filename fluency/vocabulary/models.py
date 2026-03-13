from django.db import models
from django.conf import settings
from languages.models import Language

class SavedWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    context_sentence = models.TextField(null=True, blank=True)
    source_url = models.URLField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default="learning")
    created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
