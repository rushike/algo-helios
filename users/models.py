from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db import models
from django.core.validators import RegexValidator

from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):

  def _create_user(self, first_name, last_name, email, contact_no, password, is_superuser, is_staff, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
    contact_no = contact_no.strip()
    email = self.normalize_email(email)
    user = self.model(
        first_name = first_name,
        last_name = last_name,
        email=email,
        contact_no = contact_no,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, first_name, last_name, email, contact_no, password, **extra_fields):
    return self._create_user(first_name, last_name, email, contact_no, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user("", "", email, "", password, True, True, **extra_fields)
    user.save(using=self._db)
    return user




class AlgonautsUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254, unique=True)
    contact_no = models.CharField(max_length=10) #RegexValidator(regex = r'^[0-9]*$')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)