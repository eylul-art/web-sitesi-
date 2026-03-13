from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import login_view, register_view, logout_view, index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    
    # Giriş ve Kayıt
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # Şifremi Unuttum Sistemi (4 Adım)
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]