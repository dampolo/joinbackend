from django.urls import path
from .views import get_user, get_users, create_user, delete_user, update_user

urlpatterns = [
    path('users/', get_users, name="get_users"),   # Get all users
    path('users/<int:pk>/', get_user, name="get_user"),  
    path('users/create/', create_user, name="create_user"),
    path('users/delete/<int:pk>/', delete_user, name="delete_user"),
    path('users/update/<int:pk>/', update_user, name="update_user")
]