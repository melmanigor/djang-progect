from django.contrib import admin
from django.utils.html import format_html
from .models import Vacation, Country

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('country', 'description', 'start_date', 'end_date', 'photo', 'price', 'like_count')
    list_filter = ('country',)
    search_fields = ('country__name', 'description')

    def photo(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;">',
                obj.image.url
            )
        return 'No image'
    photo.short_description = 'Image'

    def like_count(self, obj):
        return obj.liked_by.count()
    like_count.short_description = 'Likes'

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
