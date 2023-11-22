from django.contrib import admin

# Register your models here.
from .models import  *

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

#Samin
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Group)
admin.site.register(Contributor)