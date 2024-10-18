from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        
        Args:
            phone_number (str): The phone number of the user.
            password (str): The password of the user.
            **extra_fields: Additional keyword arguments to set on the user.
        
        Raises:
            ValueError: If the phone number is not provided.
        """
        if not phone_number:
            raise ValueError('The Phone Number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('taxi_driver', 'Taxi Driver'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
        
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    car_model = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number


class Order(models.Model):
    WAITING = 1
    ACCEPTED = 2
    CANCELED = 3
    STATUS_CHOICES = [
        (WAITING, 'Waiting'),
        (ACCEPTED, 'Accepted'),
        (CANCELED, 'Canceled'),
    ]

    customer = models.ForeignKey(User, related_name='customer_orders', on_delete=models.CASCADE)
    taxi_driver = models.ForeignKey(User, related_name='driver_orders', null=True, blank=True, on_delete=models.SET_NULL)
    location_from = models.CharField(max_length=255)
    location_to = models.CharField(max_length=255)
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    