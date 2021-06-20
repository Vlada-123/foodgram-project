from django.contrib import admin

from .models import Ingredient, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'slug', 'body', 'cooking_time')
    list_filter = ('author', 'title', 'cooking_time', 'tags')
    search_fields = ('title', 'body', 'tags', 'ingredients')
    ordering = ('-pub_date', 'title', 'cooking_time')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
