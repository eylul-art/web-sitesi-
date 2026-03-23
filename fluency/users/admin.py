from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserLanguageLevel

# Kullanıcının dillerini kullanıcı sayfasında "alt liste" olarak görmek için
class LanguageLevelInline(admin.TabularInline):
    model = UserLanguageLevel
    extra = 1 # Yeni dil eklemek için boş bir satır bırakır

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Kullanıcı listesinde neleri görelim?
    list_display = ('username', 'email', 'is_staff')
    
    # Kullanıcı detay sayfasında dillerini de en altta görelim
    inlines = [LanguageLevelInline]

# Seviyeleri ayrıca yönetmek istersen
@admin.register(UserLanguageLevel)
class UserLanguageLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'language_code', 'level', 'last_tested')