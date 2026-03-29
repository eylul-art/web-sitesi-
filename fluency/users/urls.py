from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- TEMEL SAYFALAR ---
    path('', views.index, name='index'),
    path('profile/', views.profile_view, name='profile'),

    # --- KİMLİK DOĞRULAMA (AUTH) ---
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- SEVİYE TESTİ YÖNLENDİRMESİ ---
    # Not: Bu URL, kullanıcıyı dillerdeki asıl sınava (languages:start_test) fırlatır.
    path('test/', views.placement_test, name='placement_test'),

    # --- ŞİFRE SIFIRLAMA İŞLEMLERİ ---
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    path('password_reset/complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),
]