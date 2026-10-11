from django.urls import path, include
from recipes.views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = 'recipes'

urlpatterns = [
    path('categories/', include([
        path('', CategoryListView.as_view(), name='category_list'),
        path('add/', CategoryCreateView.as_view(), name='category_add'),
        path('<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
        path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    ])),
]
