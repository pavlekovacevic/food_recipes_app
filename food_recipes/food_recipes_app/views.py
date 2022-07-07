from rest_framework import viewsets
from food_recipes_app import models
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from food_recipes_app import serializers
from django.db.models import Count

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""        
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user auth tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class RecipeViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description',)
    

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

class OwnRecipeViewset(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    serializer_class=serializers.RecipeSerializer

    def get_queryset(self):
            user = self.request.user
            return models.Recipe.objects.filter(user_profile=user)

class IngredientViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    serializer_class=serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()

class RatingViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    model=models.UserRating
    queryset = models.UserRating.objects.all()
    serializer_class=serializers.RatingSerializer
    
class MostUsedIngredients(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    # model=models.RecipeIngredient
    serializer_class=serializers.RecipeIngredientSerializer

    def get_queryset(self):
        most_used = models.RecipeIngredient.objects.all().values('ingredient').annotate(total=Count('ingredient')).order_by('-total')[:5]
        return most_used