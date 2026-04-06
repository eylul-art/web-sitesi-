from django.db import models
from django.conf import settings
# Diğer dosyalar bunu beklediği için geri ekledik
class Level(models.Model):
    name = models.CharField(max_length=50) # A1, A2 vb.
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)
    def __str__(self):
        return self.name

class Question(models.Model):
    language_code = models.CharField(max_length=5)
    text = models.TextField()
    level = models.CharField(max_length=2)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)
    def __str__(self):
        return f"[{self.language_code}] {self.text[:30]}"

class WritingErrorLog(models.Model):
    # 'User' yerine settings.AUTH_USER_MODEL kullanıyoruz
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    language_code = models.CharField(max_length=5)
    original_text = models.TextField()
    error_message = models.TextField()
    correct_version = models.TextField()
    error_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # username her kullanıcı modelinde olduğu için hata vermez
        return f"{self.user.username} - {self.error_type}"