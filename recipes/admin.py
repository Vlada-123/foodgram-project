from django.contrib import admin

from .models import Ingredient, MeasurementUnit, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement',)
    list_filter = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cooking_time', 'author',
                    'ingredients', 'tags', 'slug',)
    list_filter = ('author', 'name', 'tags',)
    ordering = ('-pub_date', 'name', 'cooking_time',)
    search_fields = ('name', 'description', 'tags', 'ingredients',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    ordering = ('recipe',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
