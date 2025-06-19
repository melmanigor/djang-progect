from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from typing import Optional

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email and password.

    Overrides the default ModelBackend to authenticate based on email instead of username"
    """
    def authenticate(self, request, email:str=None, password:str=None, **kwargs)->Optional[AbstractBaseUser]:
        """
        Authenticate the user using email and password.

        Args:
            request: The HTTP request object.
            email: The user's email.
            password: The user's password.
            **kwargs: Additional keyword arguments.

        Returns:
            User instance if authentication succeeds, otherwise None.
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
