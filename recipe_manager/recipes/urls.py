from django.urls import path
from .views import (
    user_register,
    user_login,
    recipe_list_create,
    recipe_detail,
    rating_create,
    recipe_search,
)

urlpatterns = [
    path('register/', user_register, name='user-register'),
    path('login/', user_login, name='user-login'),
    path('recipes/', recipe_list_create, name='recipe-list-create'),
    path('recipes/<int:pk>/', recipe_detail, name='recipe-detail'),
    path('rating/', rating_create, name='rating-create'),
    path('search/', recipe_search, name='recipe-search'),
]
