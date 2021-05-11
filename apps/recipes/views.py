from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from django.core.paginator import Paginator
from django.urls import reverse_lazy


from apps.recipes.models import Recipe, RecipeIngredient, Ingredient
# from apps.recipes.forms import RecipeForm
User = get_user_model()


class BaseRecipeList(ListView):
    context_object_name = 'recipes'
    paginate_by = 12
    template_name = None

    def get_queryset(self):
        """
        Annotate with favorite mark, select related authors.
        """
        # self.request.GET.get('tag')
        return Recipe.objects.annotate_with_favorite_prop(user_id=self.request.user.id).select_related('author')


class IndexPage(BaseRecipeList):
    template_name = 'recipes/recipes-list.html'


class AuthorRecipes(BaseRecipeList):
    template_name = 'recipes/recipes-list.html'
    some_text = 'Some text'

    def get_queryset(self):
        qs = super(AuthorRecipes, self).get_queryset()
        return qs.filter(author=self.get_user)

    @property
    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))


class FavoriteRecipes(LoginRequiredMixin, BaseRecipeList):
    """List of current user's favorite Recipes."""
    # page_title = 'Избранное'
    template_name = 'recipes/recipes-list.html'

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = qs.filter(liked_users__user=self.request.user)

        return qs

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
    # form_class = RecipeForm
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
