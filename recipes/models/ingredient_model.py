from django.db import models


class Ingredient(models.Model):
    """Модель ингредиента рецепта.

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
    unit_of_measurement = models.ForeignKey('Measurement',
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
