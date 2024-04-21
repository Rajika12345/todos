from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    options = (
        ('pending', 'pending'),
        ('completed', 'completed'),
    )
    status = models.CharField(max_length=200, choices=options, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    user_object = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
 