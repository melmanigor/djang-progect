from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from vacation.models import Vacation, Country,Like
from django.db.utils import IntegrityError
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings
# Create your tests here.
User=get_user_model()

class VacationTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@gmail.com', password='admin'
        )
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
    
    def test_admin_cannot_like_vacation(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('like_vacation', args=[self.vacation.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertNotIn(self.admin_user, self.vacation.liked_by.all())

class VacationPermissionTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@gmail.com', password='admin'
        )
        self.regular_user = User.objects.create_user(
            username='igor406', email='igor406@gmail.com', password='test12345'
        )
        self.country = Country.objects.create(name='Japan')

        image_path = os.path.join(settings.BASE_DIR, 'vacation_project', 'static', 'images', 'japan.jpg')
        with open(image_path, 'rb') as img:
            self.image_file = SimpleUploadedFile(
                name='japan.jpg',
                content=img.read(),
                content_type='image/jpeg'
            )
      

        self.vacation_data = {
            'country': self.country.id,
            'description': 'Tokyo trip',
            'start_date': (date.today() + timedelta(days=5)).isoformat(),
            'end_date': (date.today() + timedelta(days=10)).isoformat(),
            'price': '500.00',
            'image': self.image_file,
        }

    def test_admin_can_create_vacation(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('add_vacation'),
            data=self.vacation_data,
            follow=True  
    )

        

        self.assertEqual(response.status_code, 200)  
        self.assertTrue(Vacation.objects.filter(description='Tokyo trip').exists())
    
    def test_regular_user_cannot_create_vacation(self):
        self.client.force_login(self.regular_user)
        response = self.client.post(
            reverse('add_vacation'),
            data=self.vacation_data,
            follow=True
        )

        self.assertFalse(
            Vacation.objects.filter(description='Tokyo trip').exists(),
            "Regular user should not be able to create a vacation"
            )
        self.assertEqual(response.status_code, 403)
    
    def test_admin_can_update_vacation(self):
        vacation=Vacation.objects.create(
            country=self.country, 
            description='Old description', 
            start_date=date.today()+timedelta(days=5), 
            end_date=date.today()+timedelta(days=10),
            price=500, 
            image=self.image_file
            )
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('update_vacation', args=[vacation.pk]),
            {
            'country': self.country.id,
            'description': 'New desc',
            'start_date': (date.today() + timedelta(days=2)).isoformat(),
            'end_date': (date.today() + timedelta(days=6)).isoformat(),
            'price': '600.00'
        },
        follow=True
    )
        self.assertEqual(response.status_code, 200)
        vacation.refresh_from_db()
        self.assertEqual(vacation.description, 'New desc')
    def test_regular_user_cannot_update_vacation(self):
        vacation=Vacation.objects.create(
            country=self.country, 
            description='Old description', 
            start_date=date.today()+timedelta(days=5), 
            end_date=date.today()+timedelta(days=10),
            price=600, 
            image=self.image_file
            )
        update_data = {
            'country': self.country.id,
            'description': 'New desc',
            'start_date': (date.today() + timedelta(days=2)).isoformat(),
            'end_date': (date.today() + timedelta(days=6)).isoformat(),
            'price': '990.00'
        }
        self.client.force_login(self.regular_user)
        response = self.client.post(
            reverse('update_vacation', args=[vacation.pk]),
            data=update_data,
            follow=True
        )
        self.assertEqual(response.status_code, 403, "Regular user should not be able to update a vacation")
        vacation.refresh_from_db()
        self.assertNotEqual(vacation.description,'Unauthorized Update')
        self.assertNotEqual(str(vacation.price),'999')
    
    def test_admin_can_delete_vacation(self):
        vacation=Vacation.objects.create(
            country=self.country, 
            description='To Be Deleted', 
            start_date=date.today()+timedelta(days=3), 
            end_date=date.today()+timedelta(days=8),
            price=500, 
            image=self.image_file
            )
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('delete_vacation', args=[vacation.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Vacation.objects.filter(pk=vacation.pk).exists())

    def test_regular_user_cannot_delete_vacation(self):
        vacation=Vacation.objects.create(
            country=self.country, 
            description='Should Not Be Deleted', 
            start_date=date.today()+timedelta(days=3), 
            end_date=date.today()+timedelta(days=8),
            price=500, 
            image=self.image_file
            )
        self.client.force_login(self.regular_user)
        response = self.client.post(
            reverse('delete_vacation', args=[vacation.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Vacation.objects.filter(pk=vacation.pk).exists())