from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "first_name", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    
    fieldsets = (               #Shown when changing information of an existing user
        ('Details', {"fields": ("email", "password", 'first_name', 'last_name', "phone_no")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (           #Shown when creating a new User
        (None, {
            "fields": (
                "email", "password1", "password2", 'first_name', 'last_name', "phone_no", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("first_name",)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        
        if user.is_superuser:
            return qs
        return qs.filter(uuid=user.uuid)


class HotelAdmin(admin.ModelAdmin):
    model = Hotel
    list_display = ('user_id', 'name', 'address', 'rating',)
    list_filter = ('name', 'rating')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return qs
        return user.hotel_to_user.all()             #Using reverse relation by related_name

class RoomDetailAdmin(admin.ModelAdmin):
    model = RoomDetail
    list_display = ('hotel_id', 'price', 'room_type', 'description',)
    list_filter = ('price', 'room_type')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        
        if user.is_superuser:
            return qs
        return qs.filter(hotel_id__user_id__uuid = user.uuid)       #when no direct relation

class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = ('hotel_id', 'room_description', 'room_no', 'occupied',)
    list_filter = ('room_no', 'occupied')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        
        if user.is_superuser:
            return qs
        return qs.filter(hotel_id__user_id__uuid = user.uuid)       #when no direct relation

class BookingDetailAdmin(admin.ModelAdmin):
    model = BookingDetail
    list_display = ('room_id', 'user_id', 'check_in', 'check_out',)
    list_filter = (
        ('room_id', admin.RelatedOnlyFieldListFilter),
        ('user_id', admin.RelatedOnlyFieldListFilter),
        ('check_out'),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        
        if user.is_superuser:
            return qs
        # return user.bookingdetail_to_user.all()                     #Using reverse relation by related_name
        return qs.filter(room_id__hotel_id__user_id__uuid = user.uuid)
        # return qs

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomDetail, RoomDetailAdmin)
admin.site.register(BookingDetail, BookingDetailAdmin)
