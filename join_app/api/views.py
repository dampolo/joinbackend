from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from join_app.models import User

@api_view(["GET", "POST"])
def user_view(request):


    if request.method == "GET":
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            