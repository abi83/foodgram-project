import datetime
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Prefetch, Subquery, OuterRef, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, )
from django.views.generic.base import View
from django.views.generic.edit import ModelFormMixin

from apps.recipes.forms import RecipeForm
from apps.recipes.models import (
    Recipe, RecipeIngredient, Ingredient, Follow, CartItem, Tag)
from apps.recipes.paginator import FixedPaginator
from apps.recipes.utils import render_to_pdf

User = get_user_model()
logger = logging.getLogger('foodgram')


class RecipeAnnotateMixin:
    def get_queryset(self):
        """
        Annotate with favorite mark, select related authors.
        """
        query_set = super().get_queryset()
        if self.request.user.is_authenticated:
            return query_set.select_related(
                'author'
            ).annotate_with_favorite_and_cart_prop(
                user_id=self.request.user.id
            ).prefetch_related('tags')
        return query_set.select_related('author').annotate_with_session_data(
            self.request.session.get('cart')
            ).prefetch_related('tags')


class BaseRecipeList(RecipeAnnotateMixin, ListView):
    """
    A base class for recipes list classes: IndexPage, Author's page
    Favorites page
    """
    context_object_name = 'recipes'
    paginator_class = FixedPaginator
    paginate_by = 12
    template_name = 'recipes/recipes-list.html'
    page_title = None
    model = Recipe

    def get_queryset(self):
        """
        Filter by tag_breakfast, tag_lunch, tag_dinner
        URL example: http://localhost/?tags=tag_breakfast,tag_lunch,tag_dinner
        """
        query_set = (super().get_queryset()
                     .defer('description')
                     .filter(is_active=True))
        tags = self.request.GET.get('tags')
        if tags is None:
            return query_set
        tags_items = Tag.objects.filter(slug__in=tags.split(','))
        return query_set.filter(tags__in=tags_items)

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
        return (super().get_queryset()
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


class Cart(BaseRecipeList):
    template_name = 'recipes/cart.html'
    page_title = 'cart'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            cart_ids = (self.request.session.get('cart')
                        if self.request.session.get('cart')
                        else [])
            return Recipe.objects.filter(id__in=cart_ids)
        return Recipe.objects.filter(
            carts__in=CartItem.objects.filter(user=self.request.user))

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Cart items for unauthorised users
        """
        if not self.request.user.is_authenticated:
            self.extra_context = {
                'cartitems': CartItem.objects.all()[:10]
            }
        return super().get_context_data()


class RecipeDetail(RecipeAnnotateMixin, DetailView):
    template_name = 'recipes/recipe-detail.html'
    context_object_name = 'recipe'
    model = Recipe

    def get_queryset(self):
        """
        Select related ingredients
        """
        return (super().get_queryset()
                .prefetch_related('recipe_ingredients__ingredient')
                .filter(is_active=True))

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Adding 'follow' value to context
        """
        if self.request.user.is_authenticated:
            follow = Follow.objects.filter(
                author=self.object.author,
                follower=self.request.user
            ).exists()
            kwargs.update({'follow': follow})
        return super().get_context_data(**kwargs)


class RecipeIngredientSaveMixin(LoginRequiredMixin):
    @staticmethod
    def add_ingredients_to_recipe(request_data: dict, recipe):
        """
        Handle request data to create Recipe-Ingredients relation objects
        with bulk_create
        """
        # a dict for all ingredients in DB. It returns an id on 'name' key
        ingredients_dic = {ing['name']: ing['id']
                           for ing in Ingredient.objects.values('name', 'id')}
        objs = [RecipeIngredient(
            recipe=recipe,
            ingredient_id=ingredients_dic[value],
            count=request_data.get('valueIngredient_' + key.split('_')[1]),)
            for key, value in request_data.items()
            if key.startswith('nameIngredient_')
        ]
        RecipeIngredient.objects.bulk_create(objs)


class RecipeRightsCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return (self.request.user.is_superuser
                or self.request.user == self.get_object().author)


class RecipeEdit(RecipeRightsCheckMixin, RecipeIngredientSaveMixin,
                 UpdateView):
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
        self.object = form.save()
        self.add_ingredients_to_recipe(self.request.POST, self.object)
        return super(ModelFormMixin, self).form_valid(form)


class RecipeDelete(LoginRequiredMixin, RecipeRightsCheckMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:index')
    template_name_suffix = '-confirm-delete'


class Feed(LoginRequiredMixin, ListView):
    template_name = 'recipes/recipes-feed.html'
    context_object_name = 'authors'
    paginator_class = FixedPaginator
    paginate_by = 6

    def get_queryset(self):
        three_recipes_id_subquery = Subquery(
            Recipe.objects
                .filter(author_id=OuterRef('author_id'))
                .values_list('id', flat=True)[:3])
        prefetch = Prefetch(
            'recipes',
            queryset=Recipe.objects.filter(id__in=three_recipes_id_subquery), )
        return (User.objects
                .filter(following__follower=self.request.user)
                .prefetch_related(prefetch)
                .annotate(recipes_count=Count('recipes'))
                .order_by('-recipes_count'))


class ShopList(View):
    """
    A .pdf view
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            carts = CartItem.objects.filter(user=self.request.user)
            recipes = Recipe.objects.filter(carts__in=carts)
            username = request.user.get_full_name()
        else:
            recipes = Recipe.objects.filter(id__in=request.session['cart'])
            username = 'Anonymous'
        items = RecipeIngredient.objects.filter(recipe__in=recipes)
        data = {
            'time': datetime.datetime.now(),
            'number': recipes.count(),
            'customer_name': username,
            'ingredients': {},
        }
        for itm in items:
            try:  # add more count for existing ingredient
                data['ingredients'][itm.ingredient.name]['value'] += itm.count
            except KeyError:  # create new ingredient
                data['ingredients'][itm.ingredient.name] = {
                    'value': itm.count,
                    'unit': itm.ingredient.unit
                }
        pdf = render_to_pdf('recipes/shop-list.html', data)
        filename = f'Shop_list_on_{datetime.date.today()}.pdf'
        return HttpResponse(
            pdf,
            content_type='application/pdf',
            headers={'Content-Disposition': f"attachment; filename={filename}"}
        )


class Handler404(View):
    @staticmethod
    def get(request, exception):  # noqa
        logger.warning("404: page not found at {}".format(request.path))
        return render(request, 'misc/404.html',
                      {'path': request.path}, status=404)


class Handler500(View):
    @staticmethod
    def dispatch(request, *args, **kwargs):
        logger.error("500: page is broken {}".format(request.path))
        return render(request, 'misc/500.html', status=500)
