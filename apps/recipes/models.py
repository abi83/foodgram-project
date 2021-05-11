import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.db.models import Exists, OuterRef



User = get_user_model()


class Unit(models.Model):
    """
    Ingredient measure units. Eg: gram, kilogram, spoon
    """
    name = models.CharField(
        max_length=127,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Unit name',
        help_text='Ingredient measure units. Eg: gram, kilogram, spoon',
    )
    short = models.CharField(
        max_length=9,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Unit shortened name',
        help_text='Unit shortened name. Max: 9 symbols.',
    )

    class Meta:
        verbose_name = 'Ingredient unit'
        verbose_name_plural = 'Ingredient units'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Simple ingredient of recipe
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Ingredient name',
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.RESTRICT,
        related_name='Ingredient',
        blank=False,
        null=False,
        verbose_name='Ingredient unit',
        help_text='Unit for current Ingredient',
    )

    class Meta:
        verbose_name = 'Recipe ingredient'
        verbose_name_plural = 'Recipe ingredients'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def annotate_with_favorite_prop(self, user_id: int):
        return self.annotate(is_favorite=Exists(
            Favorite.objects.filter(
                user_id=user_id,
                recipe_id=OuterRef('pk'),
            ),
        ))


class Recipe(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True, verbose_name='Recipe title')
    image = models.ImageField(upload_to='recipe_images', blank=True, null=True, verbose_name='Recipe image', help_text='Image file only'    )
    slug = models.SlugField(unique=True, max_length=60, verbose_name='Recipes slug, a part of detail page URL')
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='recipes')
    time = models.PositiveIntegerField(verbose_name='Cooking time in minutes', validators=[MinValueValidator(1)])
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', blank=True)
    description = models.TextField(blank=True, null=True, help_text='Fill out description')
    tag_breakfast = models.BooleanField(default=False)
    tag_lunch = models.BooleanField(default=False, verbose_name='Обед')
    tag_dinner = models.BooleanField(default=False)
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, )
    is_active = models.BooleanField(default=True)

    objects = RecipeManager()

    def save(self, *args, **kwargs):
        """
        Trying to build a better slug
        """
        if not self.slug:
            self.slug = slugify(self.title + '-' + str(date.today()))
        try:
            super(Recipe, self).save(*args, **kwargs)
        except IntegrityError:
            self.slug = slugify(self.title + str(date.today()) + str(uuid.uuid1())[:8])
            super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Recipe instance'
        verbose_name_plural = 'Recipes instances'
        ordering = ['-pub_date', ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liked_recipes',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='liked_users',
        verbose_name='Recipe',
    )

    def __str__(self):
        return f'Liked {self.recipe} of {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Favorites object'
        verbose_name_plural = 'Favorites objects'


@receiver(pre_delete, sender=Recipe)
def delete_image(instance, **kwargs):
    instance.image.delete()


