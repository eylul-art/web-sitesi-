from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Özel kullanıcı modelini admin panelinde düzgün formlarla görmek için UserAdmin kullanıyoruz
admin.site.register(User, UserAdmin)

# Register your models here.
