from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
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
    class Priority(models.TextChoices):
        URGENT = "URGENT", _("Urgent")
        MEDIUM = "MEDIUM", _("Medium")
        LOW = "LOW", _("Low")


    class Category(models.TextChoices):
        TECHNICAL_TASK = "TECHNICAL_TASK", _("Technical Task")
        USER_STORY = "USER_STORY", _("User Story")


    class Board(models.TextChoices):
        TO_DO = "TO_DO", _("To do")
        IN_PROGRESS = "IN_PROGRESS", _("In progress")
        AWAIT_FEEDBACK = "AWAIT_FEEDBACK", _("Await feedback")
        DONE = "DONE", _("Done")

    title = models.CharField(max_length=250)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, related_name="tasks")
    due_date = models.DateField(blank=False)
    priority = models.CharField(max_length=10, choices=Priority, default=Priority.MEDIUM)
    category = models.CharField(max_length=20, choices=Category)
    board = models.CharField(max_length=20, choices=Board, default=Board.TO_DO)
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