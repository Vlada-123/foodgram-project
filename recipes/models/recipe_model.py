from autoslug import AutoSlugField
from django.db import models
from slugify import slugify

from . import Ingredient


def translate_slugify(value):
    return slugify(value)


class Recipe(models.Model):
    """Модель рецепта.

    Рецепт описывается полями:
    - Автор публикации (пользователь)
    - Название
    - Картинка
    - Текстовое описание
    - Ингредиенты: продукты для приготовления блюда по рецепту.
      Множественное поле, выбор из предустановленного списка,
      с указанием количества и единицы измерения
    - Тег (можно установить несколько тегов на один рецепт,
      выбор из предустановленных): завтрак, обед, ужин
    - Время приготовления в минутах
    - Slug (уникальная часть URL для рецепта)
    Все поля обязательны для заполнения.
    """
    author = models.ForeignKey('users.User',
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='автор')
    name = models.CharField(max_length=128,
                            verbose_name='название')
    image = models.ImageField(blank=True,
                              upload_to='static/images/recipes/%Y/%m/%d',
                              verbose_name='изображение')
    description = models.TextField(verbose_name='описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='ингредиенты')
    tags = models.ManyToManyField('Tag',
                                  related_name='recipes',
                                  verbose_name='тег',
                                  verbose_name_plural='теги')
    cooking_time = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='время приготовления'
    )
    slug = AutoSlugField(max_length=128,
                         populate_from='title',
                         slugify=translate_slugify,
                         unique_with='author__username',
                         verbose_name='slug')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    blank=True,
                                    db_index=True,
                                    verbose_name='дата публикации')

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)
