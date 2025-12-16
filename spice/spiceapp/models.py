from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now, timedelta
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True)
    phoneNumber =models.IntegerField(null=True)
    profilePic = models.ImageField(upload_to='signatures/principals/', blank=True, null=True)
    address = models.CharField(max_length=100,null=True)
    date = models.DateField(auto_now_add=True,null=True)
    balance = models.FloatField(default=10000)
    def __str__(self):
        return self.user.username
    
class Products(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True)
    bid_price=models.FloatField(default=0,null=True,blank=True)
    bid=models.IntegerField(default=0)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    quality = models.CharField(max_length=50)
    starting_price = models.IntegerField(default=0)
    reserve_price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField() 
    auction_duration = models.IntegerField()
    created = models.TimeField(null=True,blank=True)
    certified = models.CharField(max_length=50)
    description = models.TextField()
    origin = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    spice_video = models.FileField(upload_to='videos/', blank=True, null=True)
    account_number = models.CharField(max_length=20)
    ifsc = models.CharField(max_length=20)
    status=models.CharField(max_length=100,null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)
    def __str__(self):
        return self.product_name

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True)
    title=models.CharField(max_length=50)
    date=models.DateTimeField(auto_now_add=True)
    description=models.CharField(max_length=100)

    def __str__(self):
        return self.user.username +  " : " +self.title     
    
class Bids(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True)
    product = models.ForeignKey(Products,on_delete = models.CASCADE,null = True)
    # product_name = models.CharField(max_length=255)
    bid_price=models.FloatField(default=0,null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    ends_in = models.IntegerField()
    paid = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


