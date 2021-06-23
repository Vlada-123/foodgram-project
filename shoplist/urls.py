from django.urls import path

from . import views

app_name = 'shoplist'

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
         views.shoplist_download,
         name='shoplist_download'),
]
