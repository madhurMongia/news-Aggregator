from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_active', False)
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
            'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_active', False)
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                           **other_fields)
        user.set_password(password)
        user.save()
        return user
        
class newUser(PermissionsMixin,AbstractBaseUser):

    email = models.EmailField(_('email address'),unique= True)
    user_name = models.CharField(_('name'),max_length=150,unique=True)
    start_date = models.DateTimeField(default = timezone.now)
    
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name',]

    def __str__(self):
        return self.user_name
