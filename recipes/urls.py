from django.urls import path, include
from recipes.views import HomeView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, \
    RecipeCreateView, RecipeDetailView, RecipeListView, RecipeUpdateView, RecipeDeleteView

app_name = 'recipes'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', include([
        path('', CategoryListView.as_view(), name='category_list'),
        path('add/', CategoryCreateView.as_view(), name='category_add'),
        path('<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
        path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    ])),
    path('recipes/', include([
        path('', RecipeListView.as_view(), name='recipe_list'),
        path('add/', RecipeCreateView.as_view(), name='recipe_add'),
        path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
        path('<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
        path('<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    ])),
]
