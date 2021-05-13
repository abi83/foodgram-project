from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.views.generic.edit import ModelFormMixin

from apps.recipes.forms import RecipeForm
from apps.recipes.models import Recipe, RecipeIngredient, Ingredient
from apps.recipes.paginator import FixedPaginator

User = get_user_model()


class AnnotateWithFavoritesMixin:
    def get_queryset(self):
        """
        Annotate with favorite mark, select related authors.
        """
        print('AnnotateWithFavoritesMixin')
        # query_set = super().get_queryset()
        # query_set = Recipe.objects.all()
        # print('AnnotateWithFavoritesMixin2')
        return (Recipe.objects
                .annotate_with_favorite_prop(user_id=self.request.user.id)
                .select_related('author'))


class BaseRecipeList(AnnotateWithFavoritesMixin, ListView):
    """
    A base class for recipes list classes: IndexPage, Author's page
    Favorites page
    """
    context_object_name = 'recipes'
    paginator_class = FixedPaginator
    paginate_by = 12
    template_name = 'recipes/recipes-list.html'
    page_title = None

    def get_queryset(self):
        """
        Filter by tag_breakfast, tag_lunch, tag_dinner
        """
        # http://localhost/?tags=tag_breakfast,tag_lunch,tag_dinner
        # query_set = (Recipe.objects
        #     .annotate_with_favorite_prop(user_id=self.request.user.id)
        #     .select_related('author'))
        print('BaseRecipeList')
        query_set = super().get_queryset()
        # query_set = Recipe.objects.all()
        tags = self.request.GET.get('tags', None)
        if tags is None:
            return query_set
        filter_query = Q()
        for tag in tags.split(','):
            if tag in ['tag_breakfast', 'tag_lunch', 'tag_dinner']:
                filter_query.add(Q(**{tag: True}), Q.OR)
        return query_set.filter(filter_query)

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Adding a 'page_title' to context
        """
        if self._get_page_title is None:
            raise ImproperlyConfigured(
                f'"page_title" attribute of {self.__class__.__name__}'
                f' cannot be None')
        kwargs.update({'page_title': self._get_page_title})
        return super().get_context_data(**kwargs)

    @property
    def _get_page_title(self):
        return self.page_title


class IndexPage(BaseRecipeList):
    """
    A view for index page
    """
    page_title = 'Recipes'


class AuthorRecipes(BaseRecipeList):
    """
    A view for author's recipes page
    """
    def get_queryset(self):
        return (super(AuthorRecipes, self)
                .get_queryset()
                .filter(author=self.get_user))

    @property
    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    @property
    def _get_page_title(self):
        return self.get_user.get_full_name()


class FavoriteRecipes(LoginRequiredMixin, BaseRecipeList):
    """List of current user's favorite recipes."""
    template_name = 'recipes/recipes-list.html'
    page_title = 'Favorites'

    def get_queryset(self):
        """
        Favorite recipes for current user only
        """
        return (super()
                .get_queryset()
                .filter(liked_users__user=self.request.user))


class RecipeDetail(AnnotateWithFavoritesMixin, DetailView):
    template_name = 'recipes/recipe-detail.html'
    context_object_name = 'recipe'
    model = Recipe
    #TODO: annotate with favorite data


class RecipeIngredientSaveMixin(LoginRequiredMixin):
    @staticmethod
    def add_ingredients_to_recipe(request_data: dict, recipe):
        ingredients = Ingredient.objects.filter(name__in=[
            value for key, value in request_data.items()
            if 'nameIngredient' in key
        ])
        values = [request_data.get('valueIngredient_' + key.split('_')[1])
                  for key in request_data
                  if 'nameIngredient' in key]
        objs = [RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            count=value,
            )
            for ingredient, value in zip(ingredients, values)
        ]
        RecipeIngredient.objects.bulk_create(objs)


class RecipeRightsCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return (self.request.user.is_superuser
                or self.request.user == self.get_object().author)


class RecipeEdit(RecipeRightsCheckMixin, RecipeIngredientSaveMixin, UpdateView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/recipe-update.html'
    form_class = RecipeForm

    def form_valid(self, form):
        self.object = form.save()
        RecipeIngredient.objects.filter(recipe=self.object).delete()
        self.add_ingredients_to_recipe(self.request.POST, self.object)
        return super(ModelFormMixin, self).form_valid(form)


class RecipeCreate(RecipeIngredientSaveMixin, CreateView):
    model = Recipe
    success_url = reverse_lazy('recipes:index')
    template_name = 'recipes/recipe-create.html'
    form_class = RecipeForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.tag_breakfast = 'breakfast' in self.request.POST
        self.object.tag_lunch = 'lunch' in self.request.POST
        self.object.tag_dinner = 'dinner' in self.request.POST
        self.object = form.save()
        self.add_ingredients_to_recipe(self.request.POST, self.object)
        return super(ModelFormMixin, self).form_valid(form)


class RecipeDelete(LoginRequiredMixin, RecipeRightsCheckMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:index')
    template_name_suffix = '-confirm-delete'
