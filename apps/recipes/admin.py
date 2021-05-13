from django.contrib import admin
from apps.recipes.models import Unit, Ingredient, RecipeIngredient, Recipe, Favorite


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    # raw_id_fields = ('ingredient', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date', )
    list_display = ('title', 'author', )
    list_filter = ('author', )
    inlines = [IngredientInline, ]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Favorite)
class FavoriteAdmon(admin.ModelAdmin):
    pass