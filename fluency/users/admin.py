from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserLanguageLevel


class LanguageLevelInline(admin.TabularInline):
    model = UserLanguageLevel
    extra = 1 

@admin.register(User)
class MyUserAdmin(UserAdmin):
    
    list_display = ('username', 'email', 'is_staff')
    
    
    inlines = [LanguageLevelInline]


@admin.register(UserLanguageLevel)
class UserLanguageLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'language_code', 'level', 'last_tested')
