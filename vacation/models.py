from django.db import models
from user.models import User
# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=30)
    class Meta:
        db_table = 'country'
        managed = False
    def __str__(self):
        return self.country_name
class Vacation(models.Model):
    country_id=models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    file_img = models.CharField(max_length=150)
    price = models.FloatField()

    class Meta:
        db_table = 'vacations'
        managed = False
    def __str__(self):
        return f"{self.description} ({self.country}) {self.start_date} - {self.end_date}"

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacation = models.ForeignKey(Vacation, on_delete=models.DO_NOTHING, db_column='vacation_id')


    class Meta:
        db_table = 'likes'
        managed = False
        unique_together = ('user', 'vacation')

    def __str__(self):
        return f"{self.user} likes {self.vacation}"
