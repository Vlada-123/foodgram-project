from django.core.validators import MinValueValidator
from django.db import models

from . import Recipe


class Ingredient(models.Model):
    """Общая модель ингредиента рецепта.

    Данные об ингредиентах хранятся в нескольких связанных таблицах.
    На стороне пользователя ингредиент описывается полями:
    - Название
    - Количество
    - Единицы измерения
    Все поля обязательны для заполнения.
    """
    name = models.CharField(db_index=True,
                            max_length=128,
                            unique=True,
                            verbose_name='название')
    unit_of_measurement = models.ForeignKey('MeasurementUnit',
                                            null=True,
                                            on_delete=models.SET_NULL,
                                            related_name='ingredients',
                                            verbose_name='единицы измерения')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'unit_of_measurement'],
                name='unique_ingredient')
        ]
        ordering = ['name', ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.unit_of_measurement})'


class RecipeIngredient(models.Model):
    """Производная модель ингредиента конкретного рецепта."""
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredient',
                               verbose_name='рецепт')
    quantity = models.DecimalField(
        validators=[MinValueValidator(1)],
        verbose_name='количество'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe')
        ]
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты рецепта'


class MeasurementUnit(models.Model):
    """Вспомогательная модель единицы измерения для ингредиента рецепта."""
    name = models.CharField(max_length=16,
                            unique=True,
                            verbose_name='название единицы измерения')

    class Meta:
        verbose_name = 'единица измерения'
        verbose_name_plural = 'единицы измерения'

    def __str__(self):
        return self.name
