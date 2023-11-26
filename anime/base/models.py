from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(unique=True,null=True)
    bio= models.TextField(null=True,blank=True)
    address=models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=200, null=True)
    avatar= models.ImageField(null=True, default='avatar.svg')
    
    premium = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, null=True,blank=True)
    newslatter= models.BooleanField(default=False)
    

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]
    
class Product(models.Model):
    image=models.ImageField(null=True, default='avatar.svg')
    name= models.CharField(max_length=200, null=True)
    price=models.FloatField()
    instock=models.BooleanField(null=True)
    sizeclass =(
        ('S','S'),
        ('M', 'M'),
        ('L','L'),
        ('XL','XL')

    )
    size=models.CharField(max_length=20,null=True, blank=True, choices=sizeclass)
    description= models.TextField(max_length=300, null=True)
    related_anime = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cname= models.CharField(max_length=200, null=True)
    

    # paymentstatus=

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank= False)
    transaction_id= models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity= models.IntegerField(default=0, null=True, blank=True)
    date_added=  models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    Customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address= models.CharField(max_length=200, null=True)
    city= models.CharField(max_length=200, null=True)
    state= models.CharField(max_length=200, null=True)
    zipcode=models.CharField(max_length=200, null=True)
    date_added=  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address






class Location(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=350)

    def __str__(self):
        return f'{self.name} ({self.address})'

class Group(models.Model):
    group_name = models.CharField(max_length=290)

    def __str__(self):
        return f'{self.group_name}'

class Contributor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    


class Event(models.Model):
    title = models.CharField(max_length=2000)
    supervisor_email = models.EmailField()
    date = models.DateField()
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=290)
    contributor = models.ManyToManyField(Contributor, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.slug}'
