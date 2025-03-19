from rest_framework import serializers
from join_app.models import User, Task, Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ["id", 
                  "title", 
                  "description", 
                  "assigned_to", 
                  "subtasks",
                  "due_date",
                  "priority",
                  "category",
                  "board"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 
                  "name", 
                  "email", 
                  "phone",
                  "avatar_color", 
                  "created_at", 
                  "updated_at", 
                  "tasks"]
