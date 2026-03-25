from django.contrib import admin
from django.urls import path, include
from languages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')), # Kullanıcı işlemleri (login/profile/index)
    
    # 🔥 İSİM BURADA 'start_test' OLARAK TANIMLIYDI
    path('test/<str:lang_code>/', views.start_placement_test, name='start_test'),
    path('test/<str:lang_code>/evaluate/', views.evaluate_test, name='evaluate_test'),
    
    # Wikipedia ve Sözlük Modülü
    path('vocab/', include('vocabulary.urls')),
]