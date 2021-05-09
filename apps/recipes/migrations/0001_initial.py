# Generated by Django 3.2 on 2021-05-08 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Ingredient name')),
            ],
            options={
                'verbose_name': 'Recipe ingredient',
                'verbose_name_plural': 'Recipe ingredients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(blank=True, help_text='Image file only', null=True, upload_to='recipe_images', verbose_name='Recipe image')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='Recipes slug, a part of detail page URL')),
                ('description', models.TextField(blank=True, null=True)),
                ('tag_breakfast', models.BooleanField(default=False)),
                ('tag_dinner', models.BooleanField(default=False)),
                ('tag_supper', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ingredient measure units. Eg: gram, kilogram, spoon', max_length=127, unique=True, verbose_name='Unit name')),
                ('short', models.CharField(help_text='Unit shortened name. Max: 9 symbols.', max_length=9, unique=True, verbose_name='Unit shortened name')),
            ],
            options={
                'verbose_name': 'Ingredient unit',
                'verbose_name_plural': 'Ingredient units',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.ForeignKey(help_text='Unit for current Ingredient', on_delete=django.db.models.deletion.RESTRICT, related_name='Ingredient', to='recipes.unit', verbose_name='Ingredient unit'),
        ),
    ]
