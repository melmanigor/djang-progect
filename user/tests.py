from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Role

User=get_user_model()
# Create your tests here.
class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com', 
            password='testpassword12345')
    def test_login_success(self):
        response=self.client.post(reverse('login'),{
            'email': 'test@example.com',
            'password': 'testpassword12345'
        },follow=True)
                                
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_login_failure(self):
        response=self.client.post(reverse('login'),{
            'email': 'test@example.com',
            'password': 'wrongpassword'
        },follow=True)
                                
        
        self.assertEqual(response.status_code, 200)
        user=response.context.get('user')
        self.assertIsNotNone(user,"No user in response context")
        self.assertFalse(user.is_authenticated, "User is authenticated")
        self.assertContains(response, "Email or password is incorrect.")

    def test_signup_success(self):
        role=Role.objects.create(role_name='User')
        response=self.client.post(reverse('signup'),{
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpassword12345',
            'password2': 'testpassword12345',
            'role': role.id
        },follow=True)
                                
        if 'form' in response.context:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_signup_failure_due_to_existing_email(self):
        User.objects.create_user(
            username='existinguser',
            email='duplicate@example.com', 
            password='testpassword12345'
        )
        role=Role.objects.create(role_name='User')
        response=self.client.post(reverse('signup'),{
            'username': 'newuser',
            'email': 'duplicate@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpassword12345',
            'password2': 'testpassword12345',
            'role': role.id
        },follow=True)
                                
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already exists")
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_logout(self):
        self.client.login(username='testuser', password='testpassword12345')
        response=self.client.post(reverse('logout'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home'),status_code=302, target_status_code=200)