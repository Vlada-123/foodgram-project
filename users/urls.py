from django.urls import include, path

from . import views

urlpatterns = [
    path('',
         include('django.contrib.auth.urls')),
    path('register/',
         views.SignUp.as_view(),
         name='register'),
    path('subscriptions/active/',
         views.subscriptions,
         name='subscriptions'),
    path('subscriptions/<int:user_id>/',
         views.remove_subscription,
         name='remove_subscription'),
    path('subscriptions/',
         views.add_subscription,
         name='add_subscription'),
]
