from django.contrib import admin

from .models import Favorite


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    ordering = ('user',)
    search_fields = ('user',)


admin.site.register(Favorite, FavoriteAdmin)
