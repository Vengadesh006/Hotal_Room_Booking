from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import secrets
import datetime

# Create your models here.

class CustomUser(AbstractUser) : 

    email = models.EmailField(unique = True)
    
    address = models.CharField(max_length=100 , null=True , blank=True)

    moblie = models.IntegerField(default=0)

    def __str__(self) : 
        return self.username

class OTP_Token(models.Model) :
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")

    otp_code = models.CharField(max_length=6, default= secrets.token_hex(3))
    
    tp_created_at = models.DateTimeField(auto_now_add=True)

    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username

class HomePage(models.Model) : 

    title = models.CharField(max_length=200) 

    image = models.ImageField(upload_to='home')

    def __str__(self) : 
        return self.title

class Room_info(models.Model) : 

    category = models.CharField(max_length=100 , null=True)

    def __str__(self) : 
        
        return self.category

class Rooms(models.Model) : 

    head = models.CharField(max_length=100, null=True)

    price = models.FloatField(default=0, null=True)

    location = models.CharField(max_length=100 , null=True)

    image = models.ImageField(upload_to = 'room')

    def __str__(self) : 

        return self.head

class Booking(models.Model) : 
    
    user_data = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)

    room_data = models.ForeignKey(Rooms , on_delete=models.CASCADE)

    types = models.ForeignKey(Room_info , on_delete=models.CASCADE)

    check_in = models.DateField(null=False, blank=False)

    check_out = models.DateField(null=False, blank=False)

    time = models.TimeField(null=False, blank=False, default=datetime.time(12, 0))

    def __str__(self) : 

        return f'{self.user_data} has been booking the {self.room_data} as a type of Room {self.types}'


    

