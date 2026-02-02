from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils import timezone
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    login = (('email','email'),('phone','phone'),('google','google'))
    username = None 
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50,null=False,blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    login_type = models.CharField(choices=login,blank=False,null=False)

    objects = UserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

class EmailVerification(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

