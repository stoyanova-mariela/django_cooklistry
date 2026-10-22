from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, DetailView
from django.db.models.deletion import ProtectedError
from django.contrib import messages

from recipes.forms import CategoryForm, RecipeForm, RecipeIngredientFormSet
from recipes.models import Category, Recipe
from django.db import transaction
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'recipes/home.html'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'recipes/category_form.html'
    success_url = reverse_lazy('recipes:category_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'recipes/category_list.html'
    context_object_name = 'categories'


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'recipes/category_form.html'
    success_url = reverse_lazy('recipes:category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'recipes/category_confirm_delete.html'
    success_url = reverse_lazy('recipes:category_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, "This category cannot be deleted because it is used by existing recipes.")
            return HttpResponseRedirect(self.success_url)


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'ingredient_formset' not in context:
            context['ingredient_formset'] = RecipeIngredientFormSet(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()
        ingredient_formset = RecipeIngredientFormSet(request.POST, instance=self.object)

        if form.is_valid() and ingredient_formset.is_valid():
            with transaction.atomic():
                recipe = form.save()

                ingredient_formset.instance = recipe
                ingredient_formset.save()

            return redirect('recipes:recipe_detail', pk=recipe.pk)

        return self.render_to_response(self.get_context_data(form=form, ingredient_formset=ingredient_formset))


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects.select_related('category').prefetch_related('recipe_ingredients__ingredient')


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        search = self.request.GET.get('search', '').strip()
        category = self.request.GET.get('category', '')
        sort = self.request.GET.get('sort', 'az')
        queryset = Recipe.objects.select_related('category')

        if search:
            queryset = queryset.filter(title__icontains=search)

        if category.isdecimal():
            queryset = queryset.filter(category_id=int(category))

        if sort == 'za':
            return queryset.order_by('-title')
        return queryset.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_sort'] = self.request.GET.get('sort', 'az')

        return context


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'ingredient_formset' not in context:
            context['ingredient_formset'] = RecipeIngredientFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        ingredient_formset = RecipeIngredientFormSet(request.POST,instance=self.object)

        if form.is_valid() and ingredient_formset.is_valid():
            with transaction.atomic():
                recipe = form.save()
                ingredient_formset.save()
            return redirect('recipes:recipe_detail',pk=recipe.pk)

        return self.render_to_response(self.get_context_data(form=form,ingredient_formset=ingredient_formset))


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipes:recipe_list')
