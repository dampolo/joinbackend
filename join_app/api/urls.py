from django.urls import path
from .views import get_user, get_users, create_user, delete_user, update_user,\
                TaskListCreateView, TaskDetailView, create_task, update_task,\
                delete_task, get_summary

urlpatterns = [
    #USERS:
    path('users/', get_users, name="get_users"), #zostaje
    path('users/<int:pk>/', get_user, name="get_user"), # get all data from user
    path('users/', create_user, name="create_user"), #add new user
    path('users/<int:pk>/', delete_user, name="delete_user"), #delete user
    path('users/<int:pk>/', update_user, name="update_user"), #update user


    #TASKS:
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/", create_task, name="create-create"),
    path("tasks/<int:pk>/", delete_task, name="delete-detail"),
    path("tasks/<int:pk>/", update_task, name="update-detail"),

    path("summary/", get_summary, name="get-summary"),

    # path("login/", login),
    # path("registry/", registry)
    # path("logout/", logout)
]