from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import SimpleUserManager

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='viewer')
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField()
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.URLField(max_length=1000, null=True)
    
    objects = SimpleUserManager()

    REQUIRED_FIELDS = ['email', 'password']
    EMAIL_FIELD = 'email'

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['username'])
        ]

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.username
    