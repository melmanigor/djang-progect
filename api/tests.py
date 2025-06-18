from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from vacation.models import Vacation, Country, Like
from user.models import Role
from django.core.files.uploadedfile import SimpleUploadedFile

from datetime import date, timedelta

User = get_user_model()

class AuthAPITest(APITestCase):
    def setUp(self):
        self.role=Role.objects.create(role_name='user')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com', 
            password='testpassword12345',
            role=self.role
        )
        self.country=Country.objects.create(name='Greece')
        self.vacation=Vacation.objects.create(
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
    
    def test_signup_success(self):
        url=reverse('signup_api')
        response=self.client.post(url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpassword12345',
            'password2': 'testpassword12345',
            'role': self.role.id
        },format='json')
      
        self.assertEqual(response.status_code,200)
    def test_signup_failure_password_mismatch(self):
        url=reverse('signup_api')
        response=self.client.post(url, {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpassword12345',
            'password2': 'diffrentpassword',
            'role': self.role.id
        },format='json')
       
        self.assertEqual(response.status_code,400)
        self.assertIn('password',response.data)
    def test_login_success(self):
        url=reverse('login_api')
        response=self.client.post(url, {
            'email': 'test@example.com',
            'password': 'testpassword12345'
        },format='json')
        

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['detail'],'Successfully log in')
    
    def test_login_failure(self):
        url=reverse('login_api')
        response=self.client.post(url, {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        },format='json')
        self.assertEqual(response.status_code,400)
    def test_logout_authenticated_user(self):
        self.client.force_login(self.user)
        url=reverse('logout_api')
        response=self.client.post(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['detail'],'Successfully log out')
    
    def test_logout_anonymous_user(self):
        url=reverse('logout_api')
        response=self.client.post(url)
        self.assertEqual(response.status_code,403)
        
 
class VacationAPITest(APITestCase):
    def setUp(self):
        self.role=Role.objects.create(role_name='user')
        self.user = User.objects.create_user(
            username='user1',
            email='user1@example.com', 
            password='testpassword12345',
            role=self.role
        )
        self.country=Country.objects.create(name='Italy')
        self.vacation=Vacation.objects.create(
            country=self.country, 
            description='Trip to Italy', 
            start_date=date.today()+timedelta(days=10), 
            end_date=date.today()+timedelta(days=15),
            price=500, 
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=b'',
                content_type='image/jpeg'
                )
        )
    def test_vacation_list_anonymous(self):
        url=reverse('api-vacation-list')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
    
    def test_vacation_list_authenticated(self):
        self.client.force_login(self.user)
        url=reverse('api-vacation-list')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_vacation_update_by_admin(self):
        admin_role = Role.objects.create(role_name='Admin')
        admin_user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        role=admin_role
        )
        self.client.force_login(admin_user)
        url = reverse('api-vacation-update', args=[self.vacation.id])
        data = {
        'country_id': self.country.id,
        'description': 'Updated description',
        'start_date': date.today() + timedelta(days=15),
        'end_date': date.today() + timedelta(days=20),
        'price': 600.00,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Updated description')
    
    def test_vacation_update_by_regular_user(self):
        self.client.force_login(self.user)
        url = reverse('api-vacation-update', args=[self.vacation.id])
        data = {
        'country_id': self.country.id,
        'description': 'Updated description',
        'start_date': date.today() + timedelta(days=15),
        'end_date': date.today() + timedelta(days=20),
        'price': 600.00,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 403)
    
    def test_like_vacation_authenticated(self):
        self.client.force_login(self.user)
        url = reverse('like-toggle', args=[self.vacation.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_like_vacation_anonymous(self):
        url = reverse('like-toggle', args=[self.vacation.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 403)

    def test_delete_vacation_by_admin(self):
        admin_role = Role.objects.create(role_name='Admin')
        admin_user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        role=admin_role
        )
        self.client.force_login(admin_user)
        url = reverse('api-vacation-update', args=[self.vacation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    
    def test_delete_vacation_by_regular_user(self):
        self.client.force_login(self.user)
        url = reverse('api-vacation-update', args=[self.vacation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)