from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    """
    Represents a country where a vacation can take place.
    """
    name:str = models.CharField(max_length=50, unique=True)

    def __str__(self)->str:
        return self.name
class Vacation(models.Model):
    """
    Represents a vacation offered to users.
    Includes destination country, description, date range, price, image, and likes.
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    image=models.ImageField(upload_to='images/')
    price=models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10000)])
    liked_by=models.ManyToManyField(settings.AUTH_USER_MODEL,through='Like',related_name='liked_vacations')

    def __str__(self)->str:
        return f"{self.description} in {self.country.name} ({self.start_date} - {self.end_date})"

class Like(models.Model):
    """
    Represents a 'like' relationship between a user and a vacation.
    A user can like each vacation only once.
    """
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vacation=models.ForeignKey(Vacation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'vacation')

    def __str__(self)->str:
        return f"{self.user} likes {self.vacation}"