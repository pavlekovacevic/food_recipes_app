from rest_framework import serializers
from food_recipes_app import models
import requests

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
        hunter_key='48f403c690b78d5ba87e951effc5c86e4c9add96'
        email=validated_data['email']
        r = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_key}')
        response_data = r.json()['data']

        if r.status_code == 200 and response_data['status'] != 'invalid':
            """Create and return a new user"""
            user = models.UserProfile.objects.create_user(
                email=validated_data['email'],
                name=validated_data['name'],
                password=validated_data['password']
            )

            return user
        else:
            raise serializers.ValidationError("Provided email is not deliverable.")
 

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.ReadOnlyField()
    
    class Meta:
        model = models.RecipeIngredient
        fields = ('ingredient',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Ingredient
        fields=('id', 'name')

    def create(self, validated_data):
        if (not models.Ingredient.objects.filter(name=validated_data['name']).exists()):
            ingredient = models.Ingredient.objects.create(**validated_data)
            ingredient.save()

        return ingredient

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    """Serializes Recipe"""
    class Meta:
        model=models.Recipe
        fields=('id','user_profile','name', 'description', 'average_rating', 'ingredients', 'created_on')
        extra_kwargs={'user_profile':{'read_only':True}, 'ratings':{'read_only':True}}

    def create(self, validated_data):
        recipe = models.Recipe.objects.create(
            name = validated_data.get("name"),
            description = validated_data.get("description"),
            user_profile = self.context['request'].user
        )

        for ingredient in validated_data['ingredients']:
            if not models.Ingredient.objects.filter(name=ingredient['name']).exists():
                new_ingredient = models.Ingredient.objects.create(name=ingredient['name'])
                recipe.ingredients.add(new_ingredient.id)
            else:
                existing_ingredient = models.Ingredient.objects.get(name=ingredient['name'])
                mtm_relation = models.RecipeIngredient.objects.create(recipe=recipe, ingredient=existing_ingredient)
                mtm_relation.save()        
                    
        recipe.save()
        return recipe
    
    def get_average_rating(self, obj):
        ratings = models.UserRating.objects.filter(recipe=obj.id)
        average = 0

        for rating in ratings:
            average += rating.rating
        
        if average == 0:
            return 0
        else:
            return average / len(ratings)

      
class RatingSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=models.Recipe.objects.all())
    
    class Meta:
        model=models.UserRating
        fields=('id', 'rating','user_profile','recipe')
        extra_kwargs={'user_profile':{'read_only':True}}

    def create(self, validated_data):
        own_recipe = models.Recipe.objects.get(pk=validated_data.get('recipe').id) 

        if (self.context['request'].user.id == own_recipe.user_profile.id):
            raise serializers.ValidationError("You cannot rate your own recipe.")

        if (models.UserRating.objects.filter(user_profile=self.context['request'].user.id, recipe=validated_data.get('recipe').id).exists()):
            raise serializers.ValidationError("You cannot rate the same recipe more than once.")

        user_rating = models.UserRating.objects.create(
            rating=validated_data.get('rating'),
            recipe=validated_data.get('recipe'),
            user_profile=self.context['request'].user
        )

        user_rating.save()

        return user_rating
