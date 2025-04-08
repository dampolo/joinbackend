from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import UsersViewSet, TasksViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'tasks', TasksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]