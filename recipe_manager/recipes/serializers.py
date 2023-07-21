from rest_framework import serializers
from .models import User, Recipe, Ingredient, Instruction, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity')


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ('step_number', 'description')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'description', 'ingredients', 'instructions','average_rating')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instructions_data = validated_data.pop('instructions')
        user = self.context['request'].user
        recipe = Recipe.objects.create(user=user, **validated_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        for instruction_data in instructions_data:
            Instruction.objects.create(recipe=recipe, **instruction_data)

        return recipe
    
    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(recipe=obj)
        if ratings:
            average = sum([rating.rating for rating in ratings]) / len(ratings)
            return round(average, 2)
        return 0


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'recipe', 'rating')

    def create(self, validated_data):
        user = self.context['request'].user
        rating = Rating.objects.create(user=user, **validated_data)
        return rating
