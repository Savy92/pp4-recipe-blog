from . import views
from django.urls import path

urlpatterns = [
    path("", views.RecipeList.as_view(), name="home"),
    path('recipe/<int:pk>/', views.RecipeDetails.as_view(), name='recipe_detail'),
    path('like/<int:pk>/', views.LikeRecipe.as_view(), name='like_recipe'),
    path('add_recipe/', views.AddRecipe.as_view(), name='add_recipe'),
    path('recipe/edit/<int:pk>/', views.EditRecipe.as_view(), name='edit_recipe'),
]
