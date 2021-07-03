from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff')
    list_filter = ('email', 'username', 'is_active',
                   'is_staff', 'is_superuser')
    search_fields = ('email', 'username',)
    ordering = ('pk',)


admin.site.register(User, UserAdmin)
