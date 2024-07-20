from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    def remaining_time(self):
        try:
            if self.deadline > timezone.now():
                return str(self.deadline - timezone.now()).split('.')[0]
            else: return 'Expired'
        except: pass
    
    def __str__(self):
        return self.title