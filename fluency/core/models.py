from django.db import models
from django.conf import settings # User modeline güvenli erişim için

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10) # örn: en, tr, es

    def __str__(self):
        return self.name

class Level(models.Model):
    code = models.CharField(max_length=10) # örn: A1, B2

    def __str__(self):
        return self.code

class WritingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    original_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SavedWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    context_sentence = models.TextField(null=True, blank=True)
    source_url = models.URLField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default="learning") # öğreniliyor, öğrenildi vs.
    created_at = models.DateTimeField(auto_now_add=True)

class SavedMistake(models.Model):
    writing_session = models.ForeignKey(WritingSession, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    incorrect_phrase = models.CharField(max_length=255)
    suggested_correction = models.CharField(max_length=255)
    error_message = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)