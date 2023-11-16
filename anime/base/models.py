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
    
class Shop(models.Model):
    image=models.ImageField(null=True, default='avatar.svg')
    pname= models.CharField(max_length=200, null=True)
    price=models.CharField(max_length=20, null=True)
    customer_name=models.CharField(max_length=200, null=True)
    instock=models.BooleanField(null=True)
    sizeclass =(
        ('S','S'),
        ('M', 'M'),
        ('L','L'),
        ('XL','XL')

    )
    size=models.CharField(max_length=20,null=True, choices=sizeclass)
    description= models.TextField(max_length=300, null=True)

class customer(models.Model):
    cname= models.CharField(max_length=200, null=True)
    phone=models.CharField(max_length=200, null=True)
    productid= models.ForeignKey('Shop', on_delete=models.CASCADE, null=True, blank=True)
    address= models.CharField(max_length=200, null=True)
    dateofpurchase= models.DateField(auto_now_add=True)
    # paymentstatus=
