from rest_framework import permissions

from api.models import Favorite
from api.serializers import FavoriteSerializer
from api.views.views_mixins import CreateDestroyViewSet


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)
