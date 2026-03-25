from django.contrib import admin
from .models import SavedWord

@admin.register(SavedWord)
class SavedWordAdmin(admin.ModelAdmin):
    # Admin panelinde listede görünecek sütunlar
    list_display = ('word', 'turkish_meaning', 'language', 'user', 'added_at')
    
    # Sağ taraftaki filtreleme menüsü
    list_filter = ('language', 'added_at')
    
    # Arama çubuğunda neleri arayabileceği
    search_fields = ('word', 'turkish_meaning', 'user__username')
    
    # Tarih alanı sadece okunabilir olsun (elle değiştirilmesin)
    readonly_fields = ('added_at',)