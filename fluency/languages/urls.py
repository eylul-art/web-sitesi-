from django.urls import path
from . import views

urlpatterns = [
    # lang_code parametresi alan asıl test sayfası
    path('test/<str:lang_code>/', views.start_placement_test, name='start_placement_test'),
    path('evaluate/<str:lang_code>/', views.evaluate_test, name='evaluate_test'),
]