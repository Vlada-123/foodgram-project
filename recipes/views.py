import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from foodgram.settings import RECORDS_ON_PAGE

from .form import RecipeForm
from .models import (Amount, Favorite, Ingredient, Recipe, ShopList,
                     Subscription, User)
from .utils import get_ingredients, define_tags

JSON_FALSE = JsonResponse({'success': False})
JSON_TRUE = JsonResponse({'success': True})


def index(request):
    active_tags, request_tags, all_tags = define_tags(request)

    recipe_list = Recipe.objects.filter(
        tags__value__in=(request_tags or all_tags.values('value'))
    ).select_related('author').prefetch_related('tags').distinct()

    paginator = Paginator(recipe_list, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'paginator': paginator,
               'page': page,
               'all_tags': all_tags,
               'active_tags': active_tags}
    return render(request, 'index.html', context)


def profile_view(request, username):
    active_tags, request_tags, all_tags = define_tags(request)
    profile = get_object_or_404(User, username=username)

    recipes_profile = profile.recipes.filter(
        author=profile,
        tags__value__in=(request_tags or all_tags.values('value'))
    ).distinct()

    paginator = Paginator(recipes_profile, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'profile': profile,
               'paginator': paginator,
               'page': page,
               'all_tags': all_tags,
               'active_tags': active_tags}
    return render(request, 'profile.html', context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipe_main.html', context)


@login_required()
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        ingredients_add = get_ingredients(request)
        if not ingredients_add:
            return render(request, 'create_recipe.html',
                          {'form': form,
                           'new': True,
                           'errors': 'Добавьте ингредиент'})
        for title, quantity in ingredients_add.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            ingredient_item = Amount(recipe=recipe,
                                     ingredient=ingredient,
                                     quantity=quantity)
            ingredient_item.save()
        form.save_m2m()
        return redirect('recipe', recipe_id=recipe.id)
    context = {'form': form, 'new': True}
    return render(request, 'create_recipe.html', context)


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author and not request.user.is_superuser:
        return redirect('recipe', recipe_id=recipe_id)

    form = RecipeForm(request.POST,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        correct_recipe = form.save(commit=False)
        correct_recipe.save()
        correct_recipe.recipe_amount.all().delete()
        ingredients_new = get_ingredients(request)
        if not ingredients_new:
            return render(request, 'create_recipe.html',
                          {'form': form,
                           'new': False,
                           'errors': 'Добавьте ингредиент'})
        for title, quantity in ingredients_new.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            amount = Amount(recipe=correct_recipe,
                            ingredient=ingredient,
                            quantity=quantity)
            amount.save()
        form.save_m2m()
        return redirect('recipe', recipe_id=recipe.id)

    form = RecipeForm(instance=recipe)
    context = {'form': form, 'recipe': recipe, 'new': False}
    return render(request, 'create_recipe.html', context)


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user == recipe.author or request.user.is_superuser:
        recipe.delete()
        return redirect('index')
    return redirect('recipe', recipe_id=recipe_id)


@login_required
def favorites(request):
    active_tags, request_tags, all_tags = define_tags(request)
    recipe_list = Recipe.objects.filter(
        favorite_recipes__user=request.user,
        tags__value__in=(request_tags or all_tags.values('value'))
    ).distinct()

    paginator = Paginator(recipe_list, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'paginator': paginator,
               'page': page,
               'all_tags': all_tags,
               'active_tags': active_tags}
    return render(request, 'favorites.html', context)


@login_required
def following(request):
    subscription = User.objects.prefetch_related('recipes').filter(
        following__user=request.user
    )

    paginator = Paginator(subscription, RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'paginator': paginator,
               'page': page,
               'reading_to': subscription}
    return render(request, 'following.html', context)


@login_required
@require_http_methods(['GET', 'DELETE'])
def shoplist(request):
    if request.method == 'DELETE':
        recipe_id = request.GET.get('recipe_id')
        removed = ShopList.objects.get(recipe__id=recipe_id).delete()[1]
        if removed:
            return JSON_TRUE
        return JSON_FALSE
    if request.method == 'GET':
        purchases = Recipe.objects.filter(shoplist__user=request.user)
        context = {'purchases': purchases}
        return render(request, 'shoplist.html', context)


@login_required
def get_purchases(request):
    shoplist = Recipe.objects.filter(
        shoplist__user=request.user
    ).order_by(
        'ingredients__title'
    ).values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(
        total_quantity=Sum('recipe_amount__quantity')
    )

    response = HttpResponse(content_type='txt/csv')
    response['Content-Disposition'] = 'attachment; filename=shoplist.txt'
    writer = csv.writer(response)

    for item in shoplist:
        writer.writerow([f"{item['ingredients__title']} "
                         f"({item['total_quantity']} - "
                         f"{item['ingredients__dimension']})"])
    return response


@login_required
@require_http_methods(['POST', 'DELETE'])
def change_favorites(request, recipe_id):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        obj, created = Favorite.objects.get_or_create(user=request.user,
                                                      recipe=recipe)
        if not created:
            return JSON_FALSE
        return JSON_TRUE
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        removed = Favorite.objects.filter(user=request.user,
                                          recipe=recipe).delete()[1]
        if removed:
            return JSON_TRUE
        return JSON_FALSE


@login_required
@require_http_methods(['POST', 'DELETE'])
def purchases(request, recipe_id):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        obj, created = ShopList.objects.get_or_create(user=request.user,
                                                      recipe=recipe)
        if not created:
            return JSON_FALSE
        return JSON_TRUE
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        removed = ShopList.objects.filter(user=request.user,
                                          recipe=recipe).delete()[1]
        if removed:
            return JSON_TRUE
        return JSON_FALSE


@login_required
@require_http_methods(['POST', 'DELETE'])
def subscriptions(request, author_id):
    if request.method == 'POST':
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        if request.user == author:
            return JSON_FALSE
        Subscription.objects.get_or_create(user=request.user, author=author)
        return JSON_TRUE
    elif request.method == 'DELETE':
        author = get_object_or_404(User, id=author_id)
        removed = Subscription.objects.filter(user=request.user,
                                              author=author).delete()[1]
        if removed:
            return JSON_TRUE
        return JSON_FALSE
