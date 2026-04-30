from django.urls import path
from . import views

urlpatterns = [
    
    path('read/', views.wiki_reader, name='wiki_reader'),
    
    
    path('save-word/', views.save_word_ajax, name='save_word_ajax'),
    
    
    path('dictionary/', views.my_dictionary, name='my_dictionary'),
    path('update-status/<int:word_id>/', views.update_status, name='update_status'),
]
