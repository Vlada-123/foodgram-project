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
    show_name = models.CharField(max_length=32,
                                 verbose_name='отображаемый тег')
    color = models.CharField(max_length=50,
                             blank=True,
                             verbose_name='цвет')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        colors = {'breakfast': 'orange',
                  'dinner': 'purple',
                  'lunch': 'green'}
        color = colors.get(str(self.name), 'blue')
        names = {'breakfast': 'завтрак',
                 'dinner': 'ужин',
                 'lunch': 'обед'}
        show_name = names.get(str(self.name)).title()
        self.color = color
        self.show_name = show_name
        super(Tag, self).clean()

    def save(self, *args, **kwargs):
        self.clean(*args, **kwargs)
        super(Tag, self).save(*args, **kwargs)
