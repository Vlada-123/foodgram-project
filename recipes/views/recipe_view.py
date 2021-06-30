from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render, reverse

from foodgram.settings import RECORDS_ON_PAGE
from recipes.forms.recipe_form import RecipeForm
from recipes.models import Recipe, Tag
from recipes.utils import get_recipes_by_tags, save_recipe
from users.models import User

TAGS = [Tag.TagChoices.BREAKFAST,
        Tag.TagChoices.LUNCH,
        Tag.TagChoices.DINNER, ]


def home(request):
    tags = request.GET.getlist('tags', TAGS)
    recipes = get_recipes_by_tags(tags).distinct()

    paginator = Paginator(recipes, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'all_tags': Tag.objects.all(),
               'page': page,
               'paginator': paginator,
               'tags': tags, }
    return render(request, 'index.html', context)


def recipe_details(request, slug, user_id):
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    context = {'recipe': recipe}
    return render(request, 'recipe.html', context)


@login_required
def create_recipe(request):
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
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if request.user != recipe.author and not request.user.is_superuser:
        return redirect(reverse('home'))

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        author = recipe.author
        recipe = save_recipe(request, form, author)
        return redirect(reverse('recipe_detail',
                                kwargs={'slug': recipe.slug,
                                        'user_id': recipe.author.pk}))

    context = {'form': form, 'recipe': recipe}
    return render(request, 'form_recipe.html', context)


@login_required
def delete_recipe(request, slug, user_id):
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if (request.user != recipe.author) and not request.user.is_superuser:
        return redirect(reverse('home'))
    recipe.delete()
    return redirect(reverse('home'))


def profile(request, user_id):
    author = get_object_or_404(User, pk=user_id)
    tags = request.GET.getlist('tags', TAGS)
    recipes = get_recipes_by_tags(tags).filter(
        author__pk=user_id
    ).distinct()

    paginator = Paginator(recipes, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'all_tags': Tag.objects.all(),
               'author': author,
               'page': page,
               'paginator': paginator,
               'tags': tags, }
    return render(request, 'profile.html', context)


@login_required
def favorites(request):
    tags = request.GET.getlist('tags', TAGS)
    recipes = get_recipes_by_tags(tags).filter(
        favorite_by__user=request.user
    ).distinct()

    paginator = Paginator(recipes, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'all_tags': Tag.objects.all(),
               'page': page,
               'paginator': paginator,
               'tags': tags, }
    return render(request, 'index.html', context)
