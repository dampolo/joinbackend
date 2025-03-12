from django.db import models

# Create your models here.

class Task(models.Model):
    titel = models.CharField(max_length=30)
    description = models.CharField(max_length=350)
    assigned_to = models.CharField()
    due_date = models.DateField()
    prio = models.CharField()
    category = models.CharField()
    subtask = models.CharField()