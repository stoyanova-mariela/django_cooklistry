from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from meal_plans.forms import MealPlanForm
from meal_plans.models import MealPlan


class MealPlanListView(ListView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_list.html'
    context_object_name = 'meal_plans'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('recipes')


class MealPlanDetailView(DetailView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_detail.html'
    context_object_name = 'meal_plan'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('recipes')


class MealPlanCreateView(CreateView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_form.html'
    form_class = MealPlanForm
    success_url = reverse_lazy('meal_plans:meal_plan_list')


class MealPlanUpdateView(UpdateView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_form.html'
    form_class = MealPlanForm
    success_url = reverse_lazy('meal_plans:meal_plan_list')


class MealPlanDeleteView(DeleteView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_confirm_delete.html'
    success_url = reverse_lazy('meal_plans:meal_plan_list')