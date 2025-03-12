from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.



class Task(models.Model):
    titel = models.CharField(max_length=30)
    description = models.CharField(max_length=350)
    assigned_to = models.CharField(max_length=100)
    due_date = models.DateField(max_length=100)
    priority = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subtask = models.CharField(max_length=100)

class Contact(models.Model):
    name = models.CharField(max_length=50, blank=False)
    e_mail = models.EmailField(blank=False, max_length=254)
    phone = PhoneNumberField(unique=True, blank=False, region="DE")
    avatar_color = models.CharField(default="#000000")