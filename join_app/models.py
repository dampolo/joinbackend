from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.



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
    assigned_to = models.CharField(max_length=100)
    due_date = models.DateField()
    priority = models.CharField(max_length="10", choices=PRIORITY_CHOICES, default='MEDIUM')
    category = models.CharField(max_length="20", choices=CATEGORY_CHOICES)
    subtask = models.TextField()

class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False)
    e_mail = models.EmailField(blank=False, max_length=254)
    phone = PhoneNumberField(unique=True, blank=False, region="DE")
    avatar_color = models.CharField(default="#000000")