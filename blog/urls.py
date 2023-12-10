from . import views
from django.urls import path

urlpatterns = [
    path("", views.RecipeList.as_view(), name="home"),
    path('recipe/<int:pk>/', views.RecipeDetails.as_view(), name='recipe_detail'),
]
