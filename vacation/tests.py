from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from vacation.models import Vacation, Country,Like
from django.db.utils import IntegrityError
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.
User=get_user_model()

class VacationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.country = Country.objects.create(name='Greece')
        self.vacation = Vacation.objects.create(
            country=self.country, 
            description='Santorini trip', 
            start_date=date.today()+timedelta(days=5), 
            end_date=date.today()+timedelta(days=10),
            price=500, 
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=b'',
                content_type='image/jpeg'
                )
            )
        self.vacation.liked_by.add(self.user)
   
    def test_vacation_str(self):
        expected=f"Santorini trip in Greece ({self.vacation.start_date} - {self.vacation.end_date})" 
        self.assertEqual(str(self.vacation), expected)   

    def test_like_added(self):
        self.vacation.liked_by.add(self.user)
        self.assertIn(self.user, self.vacation.liked_by.all())
    def test_duplicate_like(self):
        
        with self.assertRaises(IntegrityError):
            Like.objects.create(vacation=self.vacation, user=self.user)

    
