from django.contrib import admin
from django.utils.safestring import mark_safe

from app import models


@admin.register(models.Ad)
class CarAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_url', 'make', 'model', 'year', 'price']
    list_filter = ['make', 'model', 'year', 'price']

    def show_url(self, instance):
        href = f'<a target="_blank" href={instance.url}>View on site</a>'
        return mark_safe(href)

    show_url.allow_tags = True
