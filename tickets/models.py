from django.db import models
from account.models import *
STATUS_CHOICES = [
    ('To Do', 'To Do'),
    ('In Progress', 'In Progress'),
    ('Done', 'Done'),
]
priority_choices = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]
# Create your models here.
class tickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To Do')
    priority = models.CharField(max_length=20, choices=priority_choices, default='Low')
    due_date = models.DateField(null=True, blank=True)  # ← add this

    def __str__(self):
        return f"{self.subject} - {self.user.username}"
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and self.status != 'Done':
            return self.due_date < timezone.now().date()
        return False
    