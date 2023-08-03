from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
import os
Custom_User = get_user_model()
class Custom_User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='media/', max_length=100, blank=True)
    is_premium = models.BooleanField(default=False)
    

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='blog/', blank=True)
    code = models.CharField(max_length=1000, null=True)
    date_posted = models.DateField(auto_now_add=True)
    time_posted = models.TimeField(auto_now_add=True)
    likes = models.ManyToManyField(Custom_User, related_name='liked_blogs')


    def __str__(self):
        return self.title
class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    message = models.CharField(max_length=600, blank=True)