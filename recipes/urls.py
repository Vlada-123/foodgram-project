from django.urls import path

from recipes import views

urlpatterns = [
    path('',
         views.home,
         name='home'),
    path('favorites/',
         views.favorites,
         name='favorites'),
    path('recipes/new/',
         views.create_recipe,
         name='create_recipe'),
    path('recipes/<int:user_id>/<slug:slug>/',
         views.recipe_details,
         name='recipe_details'),
    path('recipes/<int:user_id>/<slug:slug>/delete/',
         views.delete_recipe,
         name='delete_recipe'),
    path('recipes/<int:user_id>/<slug:slug>/edit/',
         views.edit_recipe,
         name='edit_recipe'),
    path('users/<int:user_id>/',
         views.profile,
         name='profile'),
]
