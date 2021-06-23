from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.shoplist_details,
         name='shoplist_details'),
    path('add/',
         views.shoplist_add,
         name='shoplist_add'),
    path('remove/<int:recipe_id>/',
         views.shoplist_remove,
         name='shoplist_remove'),
    path('download/',
         views.cart_download,
         name='shoplist_download'),
]
