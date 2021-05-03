from django.contrib import admin
from foods.models import Unit, Ingredient


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
