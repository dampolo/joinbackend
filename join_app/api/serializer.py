from rest_framework import serializers
from join_app.models import User, Task, Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'
        extra_kwargs = {"task": {"required": False}}


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    subtasks = SubtaskSerializer(many=True)

    # subtasks = SubtaskSerializer(many=True)

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
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop('assigned_to', [])

        print(f"Subtasks Data: {subtasks_data}")  # Debugging
        print(f"Assigned To Data: {assigned_to_data}")  # Debugging

        task = Task.objects.create(**validated_data)
        task.assigned_to.set(assigned_to_data)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task
    
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)
        assigned_to_data = validated_data.pop('assigned_to', None)

        # Update main Task fields
        instance = super().update(instance, validated_data)

        # Update ManyToMany field (assigned_to)
        if assigned_to_data is not None:
            instance.assigned_to.set(assigned_to_data)

        # Update subtasks
        if subtasks_data is not None:
            instance.subtasks.all().delete()  # Remove old subtasks
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=instance, **subtask_data)  # Add new subtasks

        return instance
    
    

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
