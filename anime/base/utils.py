import json
from .models import *

def cartData(request):
    if request.user.is_authenticated:
        x= Customer.objects.filter(user=request.user)
        print(x)
        if len(x) != 0:
            customer = request.user.customer
            
        else:
            customer, created = Customer.objects.get_or_create(user= request.user, cname=request.user.username)
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items


    return {'cartItems':cartItems,'order':order,'items':items}


