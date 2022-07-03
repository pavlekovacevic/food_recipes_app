from dataclasses import fields
from rest_framework import serializers
from food_recipes_app import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password':{
                'write_only': True,    
                'style':{'input_type':'password'} 
            }
        }
    
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    
    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'name')


class IngredientSerializer(serializers.ModelSerializer):
    # recipes = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model=models.Ingredient
        fields=('id', 'name')

# class RecipeIngredientSerializer(serializers.ModelSerializer):
#     pass

class RecipeSerializer(serializers.ModelSerializer):
    # ingredients = RecipeIngredientSerializer(source="recipes", many=True)
    ingredients = IngredientSerializer(many=True)

    """Serializes Recipe"""
    class Meta:
        model=models.Recipe
        fields=('id','user_profile','name', 'description', 'ingredients', 'created_on')
        extra_kwargs={'user_profile':{'read_only':True}}

    def create(self, validated_data):
        recipe = models.Recipe.objects.create(
            name = validated_data.get("name"),
            description = validated_data.get("description"),
            user_profile = self.context['request'].user
        )

        for ingredient in validated_data['ingredients']:
            new_ingredient = models.Ingredient.objects.create(name=ingredient['name'])
            recipe.ingredients.add(new_ingredient.id)

        # if "ingredients" in self.initial_data:
        #         ingredients = self.initial_data.get("ingredients")
        #         for ingredient in ingredients:
        #             id = ingredient.get("id")
        #             ingredient_instance = models.Ingredient.objects.get(pk=id)
        #             models.RecipeIngredient(recipe=recipe, ingredient=ingredient_instance).save()
        # recipe.ingredients.set(validated_data.get("ingredients"))
                    
        recipe.save()
        return recipe

      
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserRating
        fields=('id', 'rating','user_profile','recipe_id')
        extra_kwargs={'user_profile':{'read_only':True}}

