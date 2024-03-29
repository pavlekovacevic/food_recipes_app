# Generated by Django 4.0.4 on 2022-07-08 10:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_recipes_app', '0003_alter_ingredient_name_alter_recipe_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ratings',
            field=models.ManyToManyField(related_name='recipes', through='food_recipes_app.UserRating', to=settings.AUTH_USER_MODEL),
        ),
    ]
