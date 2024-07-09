from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import UserDetails

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = UserDetails.objects.get(email=email)
            if check_password(password, user.password):
                return user
        except UserDetails.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserDetails.objects.get(pk=user_id) # pk here is the primary key of the UserDetails
        except UserDetails.DoesNotExist:
            return None
