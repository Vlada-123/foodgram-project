from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse

from foodgram.settings import RECORDS_ON_PAGE
from recipes.forms.recipe_form import RecipeForm
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User

TAGS = [
    Tag.TagChoices.BREAKFAST,
    Tag.TagChoices.LUNCH,
    Tag.TagChoices.DINNER,
]


def home(request):
    """Главная страница."""
    tags = request.GET.getlist('tags', TAGS)
    recipes = Recipe.objects.filter(tags__name__in=tags).distinct()

    paginator = Paginator(recipes, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': Tag.objects.all(),
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }
    return render(request, 'index.html', context)


def recipe_details(request, slug, user_id):
    """Страница рецепта."""
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    context = {'recipe': recipe}
    return render(request, 'recipe.html', context)


def get_ingredients(request):
    """Функция получения ингредиентов. Используется при сохранении рецепта."""
    result = {}
    for key, value in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            result[value] = request.POST[f'valueIngredient_{num}']
    return result


def save_recipe(request, form, author=None, is_edit=False):
    """Сохранение рецепта. Используется при его создании и редактировании."""
    try:
        recipe = form.save(commit=False)
        recipe.author = author if author else request.user
        recipe.save()

        if is_edit:
            tmp_ingredients = RecipeIngredient.objects.filter(
                recipe=recipe
            ).delete()

        with transaction.atomic():
            ingredients = get_ingredients(request)
            recipe_ingredients = []
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=name)
                obj = RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=abs(Decimal(quantity.replace(',', '.')))
                )
                recipe_ingredients.append(obj)
            RecipeIngredient.objects.bulk_create(recipe_ingredients)
            form.save_m2m()
            return recipe

    except IntegrityError:
        if is_edit:
            RecipeIngredient.objects.bulk_create(tmp_ingredients)
        return HttpResponseBadRequest


@login_required
def create_recipe(request):
    """Создание рецепта. Требуется авторизация."""
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect(reverse('recipe_detail',
                                kwargs={'slug': recipe.slug,
                                        'user_id': recipe.author.pk}))
    context = {'form': form}
    return render(request, 'form_recipe.html', context)


@login_required
def edit_recipe(request, slug, user_id):
    """Редактирование рецепта. Требуется авторизация."""
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if request.user != recipe.author and not request.user.is_superuser:
        return redirect(reverse('home'))

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        author = recipe.author
        recipe = save_recipe(request, form, author, is_edit=True)
        return redirect(reverse('recipe_detail',
                                kwargs={'slug': recipe.slug,
                                        'user_id': recipe.author.pk}))

    context = {'form': form, 'recipe': recipe}
    return render(request, 'form_recipe.html', context)


@login_required
def delete_recipe(request, slug, user_id):
    """Удаление рецепта. Требуется авторизация."""
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if (request.user != recipe.author) and not request.user.is_superuser:
        return redirect(reverse('home'))
    recipe.delete()
    return redirect(reverse('home'))


def profile(request, user_id):
    """Страница профиля."""
    author = get_object_or_404(User, pk=user_id)
    tags = request.GET.getlist('tags', TAGS)
    recipes = Recipe.objects.filter(author__pk=user_id,
                                    tags__name__in=tags).distinct()

    paginator = Paginator(recipes, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': Tag.objects.all(),
        'author': author,
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }
    return render(request, 'profile.html', context)


@login_required
def favorites(request):
    """Избранное. Требуется авторизация."""
    tags = request.GET.getlist('tags', TAGS)
    recipes = Recipe.objects.filter(favorite_by__user=request.user,
                                    tags__name__in=tags).distinct()

    paginator = Paginator(recipes, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'all_tags': Tag.objects.all(),
        'page': page,
        'paginator': paginator,
        'tags': tags,
    }
    return render(request, 'index.html', context)
