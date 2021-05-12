from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q



from apps.recipes.models import Recipe, RecipeIngredient, Ingredient
User = get_user_model()


class BaseRecipeList(ListView):
    """
    A base class for recipes list classes: IndexPage, Author's page
    Favorites page
    """
    context_object_name = 'recipes'
    paginate_by = 12
    template_name = 'recipes/recipes-list.html'
    page_title = None

    def get_queryset(self):
        """
        Annotate with favorite mark, select related authors.
        Filter by tag_breakfast, tag_lunch, tag_dinner
        """
        # http://localhost/?tags=tag_breakfast,tag_lunch,tag_dinner
        query_set = (Recipe.objects
            .annotate_with_favorite_prop(user_id=self.request.user.id)
            .select_related('author'))
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


class RecipeDetail(DetailView):
    template_name = 'recipes/recipe-detail.html'
    context_object_name = 'recipe'
    model = Recipe


class RecipeEdit(UpdateView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/recipe-update.html'
    # form_class = RecipeForm


class RecipeCreate(CreateView):
    model = Recipe
    success_url = reverse_lazy('recipes:index')
    template_name = 'recipes/recipe-create.html'
    fields = ('title', 'time', 'description', 'image',)

    def post(self, request, *args, **kwargs):
        # breakpoint()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.tag_breakfast = 'breakfast' in self.request.POST
        self.object.tag_lunch = 'lunch' in self.request.POST
        self.object.tag_dinner = 'dinner' in self.request.POST
        self.object = form.save()
        for key in self.request.POST:
            # POST data example:
            #   'nameIngredient_1': ['...'], 'valueIngredient_1': ['200'],
            #   'unitsIngredient_1': ['г'], 'nameIngredient_3': ['...'],
            #   'valueIngredient_3': ['2'], 'unitsIngredient_3': ['шт.'],
            if 'nameIngredient' in key:
                i = key.split('_')[1]
                value = self.request.POST.get('valueIngredient_' + i)
                RecipeIngredient.objects.create(
                    recipe=self.object,
                    ingredient=Ingredient.objects.get(name=self.request.POST.get(key)),
                    count=int(value)
                )
        return super(ModelFormMixin, self).form_valid(form)
    #TODO: reformat recipe form-templates
