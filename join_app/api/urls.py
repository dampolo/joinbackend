from django.urls import path
from .views import get_user, get_users, create_user, delete_user, update_user,\
                    get_tasks, create_task, delete_task, TaskListCreateView, TaskDetailView

urlpatterns = [
    path('users/', get_users, name="get_users"),   # Get all users
    path('user/<int:pk>/', get_user, name="get_user"),  
    path('user/create/', create_user, name="create_user"),
    path('user/<int:pk>/delete/', delete_user, name="delete_user"),
    path('user/<int:pk>/update/', update_user, name="update_user"),

    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]