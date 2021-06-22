from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('recipe',)
        validators = (
            UniqueTogetherValidator(
                fields=('user', 'recipe'),
                queryset=Favorite.objects.all(),
                message=('Рецепт уже находится в избранном!')
            ),
        )
