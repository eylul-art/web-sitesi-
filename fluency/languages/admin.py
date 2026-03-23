from django.contrib import admin
from .models import Language, Level, Question

admin.site.register(Language)
admin.site.register(Level)
admin.site.register(Question)