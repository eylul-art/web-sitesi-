from django.urls import path
from . import views

urlpatterns = [
    # --- DERSLERİM (ÇOKLU DİL) YÖNETİMİ ---
    path('set-language/<int:lang_id>/', views.set_active_language, name='set_active_language'),
    path('select-language/', views.add_new_language, name='add_new_language'),

    # --- SEVİYE BELİRLEME TESTİ ---
    path('test/<str:lang_code>/', views.start_placement_test, name='start_placement_test'),
    path('evaluate/<str:lang_code>/', views.evaluate_test, name='evaluate_test'),

    # --- YAZMA PRATİĞİ (LANGUAGETOOL) ---
    path('writing/', views.writing_practice, name='writing_practice'),
    path('check-writing/', views.check_writing, name='check_writing'),
]