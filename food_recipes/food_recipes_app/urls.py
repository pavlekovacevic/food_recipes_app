from django.urls import path, include
from rest_framework.routers import DefaultRouter
from food_recipes_app import views

router=DefaultRouter()

router.register('profile', views.UserProfileViewSet)
router.register('recipes', views.RecipeViewSet)
router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('ratings', views.RatingViewSet, basename='rating')
router.register('ownrecipes', views.OwnRecipeViewset, basename='ownrecipes')
router.register('mostused', views.MostUsedIngredients, basename='mostused')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]