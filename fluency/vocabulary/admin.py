from django.contrib import admin
from .models import SavedWord

@admin.register(SavedWord)
class SavedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'user', 'language', 'status', 'created_at')
    list_filter = ('status', 'language')
    search_fields = ('word',) # Kelime arama kutusu ekler
# Register your models here.
