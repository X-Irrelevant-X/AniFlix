from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(unique=True,null=True)
    bio= models.TextField(null=True,blank=True)

    avatar= models.ImageField(null=True, default='avatar.svg')
    
    premium = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, null=True,blank=True)
    newslatter= models.BooleanField(default=False)
    

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]
    
