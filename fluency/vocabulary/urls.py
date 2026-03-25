from django.urls import path
from . import views

urlpatterns = [
    # Wikipedia okuyucu sayfası
    path('read/', views.wiki_reader, name='wiki_reader'),
    
    # Kelime kaydetme (AJAX - Arka plan işlemi)
    path('save-word/', views.save_word_ajax, name='save_word_ajax'),
    
    # 🔥 İŞTE BURASI: Hata veren 'my_dictionary' ismi tam olarak burada tanımlı
    path('dictionary/', views.my_dictionary, name='my_dictionary'),
]