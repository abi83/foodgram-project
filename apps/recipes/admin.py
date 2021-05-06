from django.contrib import admin
from apps.recipes.models import Unit, Ingredient, RecipeIngredient, Recipe


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    raw_id_fields = ('ingredient', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]
