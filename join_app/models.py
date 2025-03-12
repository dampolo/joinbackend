from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50, blank=False)
    e_mail = models.EmailField(blank=False, max_length=254)
    phone = PhoneNumberField(unique=True, blank=False, region="DE")
    avatar_color = models.CharField(max_length=10, default="#000000")

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('URGENT', 'Urgent'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    
    CATEGORY_CHOICES = [
        ('TECHNICAL_TASK', 'Technical Task'),
        ('USER_STORY', 'User Story'),        
    ]

    title = models.CharField(max_length=250)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, related_name="tasks")
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subtask = models.TextField()
    summary_place = models.CharField(max_length=5, default="to-do")

class Summary(models.Model):
    to_do = models.IntegerField(default=0)
    done = models.IntegerField(default=0)
    tasks_in_progress = models.IntegerField(default=0)
    next_task = models.IntegerField(default=0)
    await_feedback = models.IntegerField(default=0)
    tasks_on_board = models.IntegerField(default=0)

