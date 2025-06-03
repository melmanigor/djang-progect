from django.db import models
from django.conf import settings

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class Vacation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    image=models.ImageField(upload_to='images/')
    price=models.FloatField()
    liked_by=models.ManyToManyField(settings.AUTH_USER_MODEL,through='Like',related_name='liked_vacations')

    def __str__(self):
        return f"{self.description} in {self.country.name} ({self.start_date} - {self.end_date})"

class Like(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vacation=models.ForeignKey(Vacation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'vacation')

    def __str__(self):
        return f"{self.user} likes {self.vacation}"