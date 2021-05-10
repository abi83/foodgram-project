from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy


from apps.recipes.models import Recipe
from apps.recipes.forms import RecipeForm
User = get_user_model()


class IndexPage(ListView):
    paginate_by = 12
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.all()


class RecipeDetail(DetailView):
    template_name = 'recipes/recipe-detail.html'
    context_object_name = 'recipe'
    model = Recipe


class RecipeEdit(UpdateView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/recipe-update.html'
    form_class = RecipeForm


class RecipeCreate(CreateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy('recipes:index')
    template_name = 'recipes/recipe-create.html'

    def post(self, request, *args, **kwargs):
        breakpoint()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user
        # breakpoint()
        return super().form_valid(form)


class AuthorDetail(DetailView):
    template_name = 'recipes/author-page.html'
    context_object_name = 'author'
    model = User

    def get_queryset(self):
        return User.objects.filter(is_active=True) #.select_related('recipes')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        username = self.kwargs.get('username')
        author = get_object_or_404(queryset, username=username)
        return author
