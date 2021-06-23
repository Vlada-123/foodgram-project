import io
import json

import pdfkit
from django.db.models import Sum
from django.http.response import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.views.decorators.http import require_POST

from recipes.models import Recipe

from .shoplist import ShopList


@require_POST
def shoplist_add(request):
    recipe_id = json.loads(request.body).get('id')
    shoplist = ShopList(request)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    shoplist.add(recipe=recipe)
    if 'shoplist' not in request.META['HTTP_REFERER']:
        return JsonResponse({'success': True})
    return redirect('shoplist:shoplist_details')


def shoplist_remove(request, recipe_id):
    shoplist = ShopList(request)
    product = get_object_or_404(Recipe, id=recipe_id)
    shoplist.remove(product)
    if 'shoplist' not in request.META['HTTP_REFERER']:
        return JsonResponse({'success': True})
    return redirect('shoplist:shoplist_details')


def shoplist_details(request):
    shoplist = ShopList(request)
    context = {'shoplist': shoplist}
    return render(request, 'shoplist_details.html', context)


def shoplist_download(request):
    shoplist = ShopList(request)
    ids_recipes_in_purchase = [recipe['recipe'].pk for recipe in shoplist]
    recipes = Recipe.objects.filter(pk__in=ids_recipes_in_purchase).distinct()

    ingredients = recipes.order_by('ingredients__name').values(
        'ingredients__name',
        'ingredients__unit_of_measurement__name'
    ).annotate(amount=Sum('recipe_ingredient__quantity')).all()

    context = {'ingredients': ingredients}
    pdf = generate_pdf('misc/shop_list.html', context)
    return FileResponse(io.BytesIO(pdf),
                        filename='ingredients.pdf',
                        as_attachment=True)


def generate_pdf(template_name, context):
    pdf_options = {'page-size': 'A4',
                   'margin-top': '0.8in',
                   'margin-right': '0.8in',
                   'margin-bottom': '1in',
                   'margin-left': '0.8in',
                   'encoding': "UTF-8",
                   'no-outline': None, }
    html = get_template(template_name).render(context)
    return pdfkit.from_string(html, False, options=pdf_options)
