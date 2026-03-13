from django.contrib import admin
from .models import Language, Level, WritingSession, SavedWord, SavedMistake

admin.site.register(Language)
admin.site.register(Level)
admin.site.register(WritingSession)
admin.site.register(SavedWord)
admin.site.register(SavedMistake)

# Register your models here.
