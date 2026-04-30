from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    """
    Özel kullanıcı modeli. 
    Gelecekte profil resmi vb. eklemek istersen burayı kullanabilirsin.
    """
    pass

class UserLanguageLevel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="languages" # request.user.languages.all() şeklinde erişim sağlar
    )
    language_code = models.CharField(max_length=5) # 'de', 'fr' vb.
    level = models.CharField(max_length=2, default='A1')
    last_tested = models.DateTimeField(auto_now=True)
    
    # Hata aldığın kritik alan: Hangi dilin o an aktif olduğunu takip eder
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Eğer bu dil aktif yapılıyorsa, kullanıcının diğer dillerini pasif yap
        if self.is_active:
            UserLanguageLevel.objects.filter(user=self.user).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.language_code} ({self.level})"