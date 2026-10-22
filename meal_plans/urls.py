from django.urls import path, include

from meal_plans.views import MealPlanListView, MealPlanCreateView, MealPlanUpdateView, MealPlanDeleteView, MealPlanDetailView

app_name = 'meal_plans'

urlpatterns = [
    path('', MealPlanListView.as_view(), name='meal_plan_list'),
    path('create/', MealPlanCreateView.as_view(), name='meal_plan_create'),
    path('<int:pk>/', include([
        path('', MealPlanDetailView.as_view(), name='meal_plan_detail'),
        path('edit/', MealPlanUpdateView.as_view(), name='meal_plan_edit'),
        path('delete/', MealPlanDeleteView.as_view(), name='meal_plan_delete'),
    ]))
]
