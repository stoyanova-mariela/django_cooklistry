from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.db.models.deletion import ProtectedError
from django.contrib import messages

from recipes.forms import CategoryForm
from recipes.models import Category


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
