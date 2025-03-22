from rest_framework import serializers
from join_app.models import User, Task, Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    subtasks = SubtaskSerializer(many=True)

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
        
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        print(f"Subtasks Data: {subtasks_data}")  # Debugging

        task = Task.objects.create(**validated_data)
        print(f"Created Task: {task}")  # Debugging


        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task


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
