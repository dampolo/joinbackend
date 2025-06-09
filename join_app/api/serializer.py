from rest_framework import serializers
from join_app.models import Contact, Task, Subtask
from join_app.validators import CustomPhoneValidator

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    phone = serializers.CharField(write_only=False)

    class Meta:
        model = Contact
        fields = ["id", 
                  "name", 
                  "email",
                  "phone",           # <- Added here
                  "avatar_color", 
                  "created_at", 
                  "updated_at", 
                  "tasks"]
        extra_kwargs = {
            "tasks": {"required": False},
            "phone": {"required": False}
        }

    def validate_phone(self, value):
        validator = CustomPhoneValidator()
        validator(value)

        contact_id = self.instance.id if self.instance else None
        if Contact.objects.filter(phone=value).exclude(id=contact_id).exists():
            raise serializers.ValidationError("This phone exists already.")
        return value


class SubtaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Subtask
        fields = ['id', 'description', 'completed']
        extra_kwargs = {"task": {"required": False}}


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Contact.objects.all()
    )

    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = ["id", 
                  "title", 
                  "description", 
                  "assigned_to", 
                  "due_date",
                  "priority",
                  "category",
                  "board",
                  "subtasks",]
        
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop('assigned_to', [])

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

        # Update subtasks (no delete+recreate)
        if subtasks_data is not None:
            existing_subtasks = {sub.id: sub for sub in instance.subtasks.all()}
            sent_ids = []

            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id', None)
                if subtask_id and subtask_id in existing_subtasks:
                    sub = existing_subtasks[subtask_id]
                    sub.description = subtask_data.get('description', sub.description)
                    sub.completed = subtask_data.get('completed', sub.completed)
                    sub.save()
                    sent_ids.append(subtask_id)
                else:
                    new_sub = Subtask.objects.create(task=instance, **subtask_data)
                    sent_ids.append(new_sub.id)
        
        for sub_id in existing_subtasks:
            if sub_id not in sent_ids:
                existing_subtasks[sub_id].delete()

        return instance

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["assigned_to"] = [{"id": user.id, "name": user.name} for user in instance.assigned_to.all()]
        return rep
    
