from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Case, File

class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('user', 'created_at', 'updated_at')

admin.site.register(Case, CaseAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('case', 'created_at', 'updated_at')

admin.site.register(File, FileAdmin)
