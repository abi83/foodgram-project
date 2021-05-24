import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Exists, OuterRef, Value
from django.db.models.expressions import Case, When
from django.db.models.signals import pre_delete
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from apps.recipes.utils import get_first_user_id

User = get_user_model()


class Unit(models.Model):
    """
    Ingredient measure units. Eg: gram, kilogram, spoon
    """
    name = models.CharField(
        max_length=127,
        unique=True,
        verbose_name='Unit name',
        help_text='Ingredient measure units. Eg: gram, kilogram, spoon',
    )
    short = models.CharField(
        max_length=9,
        unique=True,
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
        db_index=True,
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.RESTRICT,
        related_name='Ingredient',
        verbose_name='Ingredient unit',
        help_text='Unit for current Ingredient',
    )

    class Meta:
        verbose_name = 'Recipe ingredient'
        verbose_name_plural = 'Recipe ingredients'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    def annotate_with_favorite_and_cart_prop(self, user_id: int):
        return self.annotate(is_favorite=Exists(
            Favorite.objects.filter(user_id=user_id, recipe_id=OuterRef('pk')),
        )).annotate(in_cart=Exists(
            CartItem.objects.filter(user_id=user_id, recipe_id=OuterRef('pk')))
        )

    def annotate_with_session_data(self, recipes_ids: list):
        recipes_ids = recipes_ids if recipes_ids is not None else []
        return self.annotate(
            in_cart=Case(When(id__in=recipes_ids, then=True))
            ).annotate(is_favorite=Value(False))


class Recipe(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Recipe title'
    )
    image = models.ImageField(
        upload_to='recipe_images',
        blank=True,
        null=True,
        verbose_name='Recipe image',
        help_text='Image file only'
    )
    slug = models.SlugField(
        unique=True,
        max_length=60,
        verbose_name='Recipes slug, a part of detail page URL',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=get_first_user_id,
        related_name='recipes'
    )
    time = models.PositiveIntegerField(
        verbose_name='Cooking time in minutes',
        validators=[MinValueValidator(1), ]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        blank=True,
        help_text='Fill out some ingredients and it"s values'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Fill in the description'
    )
    # TODO: refactor this!
    tag_breakfast = models.BooleanField(
        default=False,
        verbose_name='Breakfast',
        help_text='Select if this recipe is suitable for breakfast'
    )
    tag_lunch = models.BooleanField(
        default=False,
        verbose_name='Lunch',
        help_text='Select if this recipe is suitable for lunch',
    )
    tag_dinner = models.BooleanField(
        default=False,
        verbose_name='Dinner',
        help_text='Select if this recipe is suitable for dinner',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = 'Recipe instance'
        verbose_name_plural = 'Recipes instances'
        ordering = ['-pub_date', ]

    def save(self, *args, **kwargs):
        """
        Trying to build a better slug
        """
        if not self.slug:
            self.slug = slugify(self.title + '-' + str(date.today()))
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = slugify(
                self.title + str(date.today()) + str(uuid.uuid1())[:8])
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipes:recipe-detail', args=[self.slug, ])

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """
    A recipe-ingredient M2M relation model with count value.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )


@receiver(pre_delete, sender=Recipe)
def delete_image(instance, **kwargs):
    instance.image.delete()


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Favorites object'
        verbose_name_plural = 'Favorites objects'

    def __str__(self):
        return f'Liked {self.recipe} of {self.user}'


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        verbose_name='Someone who follows the author',
        related_name='followers',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author to follow',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Follow instance'
        verbose_name_plural = 'Follow instances'
        constraints = [
            models.UniqueConstraint(fields=['follower', 'author'],
                                    name='twice_follow_impossible')]


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Cart\'s user',
        related_name='shopitems',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe in cart',
        related_name='carts', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Recipe in cart relation'
        verbose_name_plural = 'Recipe in cart relations'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe', ],
                                    name='two_recipes_in_one_cart_impossible')
        ]
