from django.db import models
from django.conf import settings

class SavedWord(models.Model):
    
    STATUS_CHOICES = [
        ('learning', 'Öğreniyorum ⏳'),
        ('review', 'Tekrar Et 🔄'),
        ('learned', 'Öğrendim ✅'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    turkish_meaning = models.CharField(max_length=150, blank=True, null=True) 
    language = models.CharField(max_length=5)
    
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='learning')
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.word} ({self.turkish_meaning}) - {self.get_status_display()}"
