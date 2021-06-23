from django.core.validators import MinValueValidator
from django.db import models

from . import Ingredient, Recipe


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
        max_digits=5,
        decimal_places=1,
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
