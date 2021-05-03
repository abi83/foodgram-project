from django.db import models


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

    def __str__(self):
        return f'Unit: {self.name}'


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
        return f'Ingredient: {self.name}'
