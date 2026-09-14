from django.contrib import admin
from .models import Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'emoji', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'short_description', 'full_description')
    ordering = ('order', 'name')
