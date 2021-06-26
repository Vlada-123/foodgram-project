from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('author/',
         views.AboutAuthorView.as_view(),
         name='author'),
    path('technologies/',
         views.AboutTechnologiesView.as_view(),
         name='technologies'),
]
