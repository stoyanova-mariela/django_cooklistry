from django.urls import path, include
from ingredients.views import IngredientListView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView

app_name = 'ingredients'

urlpatterns = [
    path('', IngredientListView.as_view(), name='ingredient_list'),
    path('add/', IngredientCreateView.as_view(), name='ingredient_add'),
    path('<int:pk>/', include([
        path('edit/', IngredientUpdateView.as_view(), name='ingredient_edit'),
        path('delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),
    ]))
]