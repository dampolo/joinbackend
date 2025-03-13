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
        return self.name

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
        ("TO_DO", "to-do"),
        ("IN_PROGRESS", "in-progress"),
        ("AWAIT_FEEDBACK", "await-feedback"),
        ("DONE", "done"),
    ]

    title = models.CharField(max_length=250)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, related_name="tasks")
    due_date = models.DateField(blank=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subtask = models.TextField()
    summary_place = models.CharField(max_length=20, choices=BOARD_CHOICES, default="to-do")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task")
    completed= models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Summary(models.Model):
    to_do = models.IntegerField(default=0)
    done = models.IntegerField(default=0)
    tasks_in_progress = models.IntegerField(default=0)
    next_task = models.IntegerField(default=0)
    await_feedback = models.IntegerField(default=0)
    tasks_on_board = models.IntegerField(default=0)

