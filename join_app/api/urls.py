from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UsersViewSet, TasksViewSet

router = SimpleRouter()
router.register(r'users', UsersViewSet, basename="users")  # Users routes
router.register(r'tasks', TasksViewSet, basename="tasks")  # Tasks routes

urlpatterns = [
    path("", include(router.urls)),
]