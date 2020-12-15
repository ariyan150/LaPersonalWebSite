from django.db import models
from django.contrib.auth.models import User

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todolost', null=True)
    name = models.CharField(max_length=200)
    detail = models.CharField(max_length=500, null=True)
    category = models.CharField(max_length=200, null=True)
    added_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
