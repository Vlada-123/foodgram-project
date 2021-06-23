from django.conf import settings

from recipes.models import Recipe


class ShopList:
    def __init__(self, request):
        self.session = request.session
        shoplist = self.session.get(settings.SHOPLIST_SESSION_NAME)
        if not shoplist:
            shoplist = self.session[settings.SHOPLIST_SESSION_NAME] = {}
        self.shoplist = shoplist

    def add(self, recipe, quantity=1, update_quantity=False):
        recipe_id = str(recipe.id)
        if recipe_id not in self.shoplist:
            self.shoplist[recipe_id] = {'quantity': 1}
            if update_quantity:
                self.shoplist[recipe_id]['quantity'] = quantity
            else:
                self.shoplist[recipe_id]['quantity'] += quantity
            self.save()

    def remove(self, recipe):
        recipe_id = str(recipe.id)
        if recipe_id in self.shoplist:
            del self.shoplist[recipe_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        recipe_ids = self.shoplist.keys()
        recipes = Recipe.objects.filter(id__in=recipe_ids)
        cart = self.shoplist.copy()
        for recipe in recipes:
            cart[str(recipe.id)]['recipe'] = recipe
        for item in cart.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.shoplist.values())

    def clear(self):
        del self.session[settings.SHOPLIST_SESSION_NAME]
        self.save()
