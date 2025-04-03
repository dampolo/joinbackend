from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import UsersViewSet, TasksViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename="users")  # Users routes
router.register(r'tasks', TasksViewSet, basename="tasks")  # Tasks routes

urlpatterns = [
    path("", include(router.urls)),
]