from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=20)
    class Meta:
        db_table = 'roles'
        managed = False
        


    def __str__(self):
        return self.role_name

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role=models.CharField(max_length=20)
    
    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name}"