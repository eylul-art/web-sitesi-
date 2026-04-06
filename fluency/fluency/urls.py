from django.contrib import admin
from django.urls import path, include  # include eklendi
from languages import views            # languages views eklendi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')), # Kullanıcı işlemleri (login/profile/index)
    
    # 🔥 İSİM BURADA 'start_test' OLARAK TANIMLIYDI
    path('test/<str:lang_code>/', views.start_placement_test, name='start_test'),
    path('test/<str:lang_code>/evaluate/', views.evaluate_test, name='evaluate_test'),
    
    # Wikipedia ve Sözlük Modülü
    path('vocab/', include('vocabulary.urls')),
    
    # Yazma Pratiği Modülü (lang_views karmaşası düzeltildi, hepsi tek views'ten çekiliyor)
    path('writing/', views.writing_practice, name='writing_practice'),
    path('check-writing/', views.check_writing, name='check_writing')
]