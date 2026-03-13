from django.contrib import admin
from .models import WritingSession, SavedMistake

@admin.register(WritingSession)
class WritingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'created_at')
    list_filter = ('language', 'user') # Yan tarafta filtreleme paneli açar

@admin.register(SavedMistake)
class SavedMistakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'incorrect_phrase', 'suggested_correction', 'updated_at')
# Register your models here.
