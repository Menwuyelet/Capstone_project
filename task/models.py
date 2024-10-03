from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]

    title = models.CharField(max_length=50, unique = True)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length = 10, choices = PRIORITY_CHOICES)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'Pending')
    completed_at = models.DateField(null = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank = True)

    def __str__(self):
        return self.title
