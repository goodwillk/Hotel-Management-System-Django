import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

from django.core.validators import MinValueValidator, MaxValueValidator


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class CustomUser(AbstractUser, BaseModel):
    email = models.EmailField('email address', unique=True)
    phone_no = models.BigIntegerField(unique=True)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_no", ]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
class Hotel(BaseModel):
    user_id = models.ForeignKey(CustomUser, related_name='hotel_to_user', on_delete = models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=300, unique=True)
    description = models.TextField(max_length=1000)
    rating = models.IntegerField(default=1 ,validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def __str__(self):
        return self.name


class RoomDetail(BaseModel):
    hotel_id = models.ForeignKey(Hotel, related_name='roomdetail_to_hotel', on_delete = models.CASCADE)
    price = models.IntegerField(default=0)
    room_type = models.CharField(max_length=100, default='Regular')
    description = models.TextField(max_length=1000)
    images = models.ImageField(null=True) 
    
    def __str__(self):
        return f"Room details of {self.room_type} type Room of {self.hotel_id}"


class Room(BaseModel):
    hotel_id = models.ForeignKey(Hotel, related_name='room_to_hotel', on_delete = models.CASCADE)
    room_description = models.ForeignKey(RoomDetail, related_name='room_to_roomdetail', on_delete = models.CASCADE)
    room_no = models.SmallIntegerField()
    occupied = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Room Number - {self.room_no} of {self.hotel_id.name} "
    
    class Meta:
        unique_together = ['room_no', 'hotel_id']

    
class BookingDetail(BaseModel):
    room_id = models.ForeignKey(Room, related_name='bookingdetail_to_room', on_delete = models.CASCADE)
    user_id = models.ForeignKey(CustomUser, related_name='bookingdetail_to_user', on_delete = models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Booking details of {self.room_id}"
    
