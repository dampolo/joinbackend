from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import UserSerializer, TaskSerializer
from join_app.models import User, Task


# Get a single user:
@api_view(["GET"])
def get_user(request, pk):
    if request.method == "GET":
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Get all users:
@api_view(["GET"])
def get_users(request):
    if request.method == "GET":
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

# Create new user
@api_view(["POST"])
def create_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

# Delete user
@api_view(["GET", "DELETE"])
def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    serializer = UserSerializer(user)
    
    if request.method == "GET":
        return Response(serializer.data)
    
    if request.method == "DELETE":
        user.delete()
        return Response(serializer.data)

# Update user
@api_view(["GET", "PUT"])
def update_user(request, pk):
    
    if request.method == "GET":
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    if request.method == "PUT":
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
