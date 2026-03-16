from django.contrib import admin
from django.urls import path, include # include eklemeyi unutma!

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Tüm kullanıcı işlemlerini 'users' uygulamasındaki urls.py'ye paslıyoruz
    path('', include('users.urls')), 
]