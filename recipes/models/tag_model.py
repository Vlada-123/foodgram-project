from django.db import models


class Tag(models.Model):
    """Модель тега для рецепта.

    Для рецепта можно установить несколько тегов.
    Теги выбираются из предустановленных.
    """

    class TagChoices(models.TextChoices):
        BREAKFAST = ('breakfast', 'завтрак')
        LUNCH = ('lunch', 'обед')
        DINNER = ('dinner', 'ужин')

    name = models.CharField(choices=TagChoices.choices,
                            max_length=16,
                            unique=True,
                            verbose_name='название тега')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name
