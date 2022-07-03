from django.contrib import admin
from food_recipes_app import models

admin.site.register(models.UserProfile)
admin.site.register(models.Recipe)