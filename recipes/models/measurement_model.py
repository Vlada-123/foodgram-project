from django.db import models


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
