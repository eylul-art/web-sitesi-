from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Kullanıcı işlemleri (login/profile/index)
    path('', include('users.urls')), 
    
    # Wikipedia ve Sözlük Modülü
    path('vocab/', include('vocabulary.urls')),
    
    # 🔥 İŞTE ÇÖZÜM: Yazma Pratiği, Testler, Ders Ekleme ve Seçme İşlemleri
    # Bunların hepsini zaten languages/urls.py içine yazmıştık, oradan çekiyoruz.
    path('', include('languages.urls')), 
]