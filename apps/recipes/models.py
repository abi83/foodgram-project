from django.db import models
from django.contrib.auth import get_user_model

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


class Recipe(models.Model):
    title = models.CharField(max_length=255, blank=False, null=True)
    image = models.ImageField(upload_to='recipe_images', blank=True, null=True, verbose_name='Recipe image', help_text='Image file only')
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT,
                               default=1)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    description = models.TextField(blank=True, null=True)
    tag_breakfast = models.BooleanField(default=False)
    tag_dinner = models.BooleanField(default=False)
    tag_supper = models.BooleanField(default=False)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
