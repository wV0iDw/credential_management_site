from django.db import models
from .models import*
from datetime import datetime

# Create your models here.
class CustomUser(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    image = models.ImageField(upload_to='images/',default=None)
    role_id = models.IntegerField(default=None)
    address = models.TextField(null=True)
    login_ip_address = models.CharField(max_length=200)
    login_datetime = models.DateTimeField(default=datetime.now(), blank=True)
    login_otp = models.CharField(max_length=200,null=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Roles(models.Model):
    name= models.CharField(max_length=50)
    status= models.IntegerField(default=1)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


class website_credentials(models.Model):
    user_ids = models.CharField(max_length=100)
    website_name = models.CharField(max_length=200) 
    website_host = models.CharField(max_length=200) 
    website_ip = models.CharField(max_length=200)
    website_username = models.CharField(max_length=50) 
    website_password = models.CharField(max_length=50) 
    added_by = models.CharField(max_length=100,null=True)
    updated_by = models.CharField(max_length=100,null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status= models.IntegerField(default=1)


class histories(models.Model):
    user_Id = models.IntegerField()
    login_date = models.DateField(auto_now_add=True)
    login_time = models.TimeField()
    login_ip_address = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class permissions(models.Model):
    role_id = models.IntegerField()
    permission = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
   
