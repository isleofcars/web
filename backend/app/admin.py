from django.contrib import admin
from django.utils.safestring import mark_safe

from app import models


@admin.register(models.CarAdvertisement)
class CarAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_url', 'make', 'model', 'year', 'price']
    list_filter = ['make', 'model', 'year', 'price']

    def show_url(self, instance):
        return mark_safe(f'<a target="_blank" href={instance.url}>View on site</a>')

    show_url.allow_tags = True
