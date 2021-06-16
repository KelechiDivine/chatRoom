from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.

class CustomerUserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError("Email field is required")
        
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_acive', True)
        extra_fields.setdefault('name', 'admin')
        
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff= True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser= True.')
        
        

