from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.db import models
import uuid

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("El email es obligatorio.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)



class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('viewer', 'Viewer'),
    ]

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email            = models.EmailField(unique=True)
    username         = models.CharField(max_length=150, blank=True)
    role             = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    avatar_url       = models.URLField(max_length=500, blank=True, null=True)
    avatar_public_id = models.CharField(max_length=500, blank=True, null=True)

    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username 
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
