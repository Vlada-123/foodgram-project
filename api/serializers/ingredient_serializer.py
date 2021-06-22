from rest_framework import serializers

from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    unit_of_measurement = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = Ingredient
        fields = '__all__'
