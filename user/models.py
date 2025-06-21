from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    """
    Model representing a user role (e.g., Admin, User, etc.).
    """
    role_name:str = models.CharField(max_length=20)
    
    def __str__(self):
        
        return self.role_name

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser,
    with an additional role field linked to the Role model.
    """
    role:Role = models.ForeignKey(Role, on_delete=models.CASCADE , null=True, blank=True)
    def __str__(self):
        return f"{self.username} {self.role}" if self.role else self.username