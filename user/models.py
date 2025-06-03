from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    role_name = models.CharField(max_length=20)
    
    def __str__(self):
        
        return self.role_name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE , null=True)
    def __str__(self):
        return f"{self.username} {self.role}"