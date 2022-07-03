from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email adress!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given credentials"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    last_login = models.DateField(verbose_name='last login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retreive full name of user"""
        return self.name

    def get_short_name(self):
        """Retreive short name of user"""
        return self.name

    def __str__(self):
        """return string representation of our user """
        return self.email



class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name='recipes', through="RecipeIngredient")
    created_on = models.DateTimeField(auto_now_add=True)
    user_profile=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING 
    )
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class UserRating(models.Model):
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING 
    )
    recipe = models.ForeignKey(on_delete = models.DO_NOTHING, to=Recipe)
    rating =  models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
     )


