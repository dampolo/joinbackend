from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializer import UserSerializer, TaskSerializer, SubtaskSerializer
from join_app.models import User, Task, Subtask


class UsersViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        user.delete()
        return Response(serializer.data)


class TasksViewSet(viewsets.ViewSet):
    pass

# Handles both GET (list) and POST (create)
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Handles GET (single task), PUT/PATCH (update), and DELETE (delete)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer