import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods, require_POST

from foodgram import settings
from users.models import Connection, User


@login_required
def subscriptions(request):
    """Подписки."""
    user_from = request.user
    authors = user_from.following.all().prefetch_related('recipes').annotate(
        recipe_count=Count('recipes')
    ).order_by('username')

    paginator = Paginator(authors, settings.RECORDS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator, }
    return render(request, 'subscriptions.html', context)


@login_required
@require_POST
def add_subscription(request):
    """Добавление подписки."""
    user_id = json.loads(request.body).get('id')
    user_to = get_object_or_404(User, id=user_id)
    user_from = request.user

    if Connection.objects.filter(user_to=user_to,
                                 user_from=user_from).exists():
        return JsonResponse({'success': False})
    Connection(user_to=user_to, user_from=user_from).save()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['DELETE', ])
def remove_subscription(request, user_id):
    """Удаление подписки."""
    user_to = get_object_or_404(User, id=user_id)
    user_from = request.user

    if not Connection.objects.filter(user_to=user_to,
                                     user_from=user_from).exists():
        return JsonResponse({'success': False})
    Connection.objects.get(user_to=user_to, user_from=user_from).delete()
    return JsonResponse({'success': True})
