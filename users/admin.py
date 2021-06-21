from django.contrib import admin

from .models import Connection, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('email', 'username',)
    ordering = ('pk',)
    search_fields = ('email', 'username',)


class ConnectionAdmin(admin.ModelAdmin):
    date_hierarchy = ('created',)
    list_display = ('user_from', 'user_to', 'created',)
    list_filter = ('user_from', 'user_to', 'created',)
    ordering = ('created', 'user_from',)
    search_fields = ('user_from', 'user_to',)


admin.site.register(User, UserAdmin)
admin.site.register(Connection, ConnectionAdmin)
