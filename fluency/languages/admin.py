from django.contrib import admin
from .models import Language, Level

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code') # Tablo listesinde görünecek sütunlar

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('code',)
    

# Register your models here.
