# Generated by Django 4.0.4 on 2022-07-06 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_recipes_app', '0002_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
