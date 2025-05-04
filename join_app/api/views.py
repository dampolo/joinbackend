from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from .serializer import UserSerializer, TaskSerializer
from join_app.models import Contact, Task


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]