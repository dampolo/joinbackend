from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, max_length=254, blank=False)
    phone = PhoneNumberField(unique=True, blank=False, region="DE")
    avatar_color = models.CharField(max_length=10, default="#000000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("URGENT", "Urgent"),
        ("MEDIUM", "Medium"),
        ("LOW", "Low"),
    ]
    
    CATEGORY_CHOICES = [
        ("TECHNICAL_TASK", "Technical Task"),
        ("USER_STORY", "User Story"),        
    ]

    BOARD_CHOICES = [
        ("TO_DO", "To do"),
        ("IN_PROGRESS", "In progress"),
        ("AWAIT_FEEDBACK", "Await feedback"),
        ("DONE", "Done"),
    ]

    title = models.CharField(max_length=250)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, related_name="tasks")
    due_date = models.DateField(blank=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    board = models.CharField(max_length=20, choices=BOARD_CHOICES, default="TO_DO")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.priority}"
#
class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task")
    completed= models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)