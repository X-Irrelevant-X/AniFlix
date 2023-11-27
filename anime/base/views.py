from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login,logout

from .models import  *
from .forms import MyUserCreationForm, UserForm
from django.http import JsonResponse
import json
from .utils import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from .utils import cartData

from django.views.decorators.csrf import csrf_exempt
import datetime
from sslcommerz_lib import SSLCOMMERZ 


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)
        except:
            return HttpResponse("Fuck off you are not a registered user")
        user=authenticate(request,email=email, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("username or password incorrect")
    context={'page':page}
    return render(request,'base/login-register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data["email"]
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login-register.html', {'form': form})


def Home(request):

    user = request.user

    
    context={
        'user':user,
        }

    return render(request,'base/home.html',context)

def userProfile(request,pk):

    user=User.objects.get(id=pk)
    

    context={'user':user,}
    return render(request,'base/profile.html',context)


def notification(request):
    user = request.user
    contributor, _ = Contributor.objects.get_or_create(user=user)
    events,_ = Event.objects.filter(contributor=user)

    context = {'user': user, 'events': events}
    return render(request, 'base/updates.html', context)

@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method == 'POST':
        form=UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request,'base/update-user.html',{'form':form})

@login_required(login_url='/accounts/login/')
def shop(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    
    sort_by = request.GET.get('sort_by', 'default')
    search_query = request.GET.get('q', '')
    
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(related_anime__icontains=search_query))
        
    # Sort the products based on the sorting parameter
    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')
    elif sort_by == 'new_arrival':
        products = list(reversed(products))

    paginator = Paginator(products, 6)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'cartItems': cartItems,
        'sort_by': sort_by,
    }

    return render(request, 'store/shop.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer, created = Customer.objects.get_or_create(user=request.user, cname=request.user.username)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    if orderItem.quantity <= 0:
        orderItem.delete() 
    else:
        orderItem.save()

    cart_total = order.get_cart_items
    cart_totalPrice = order.get_cart_total

    response_data = {
        'message': 'Item was added',
        'cartItems': cart_total,
        'itemQuantity': orderItem.quantity,
        'cartTotal': order.get_cart_total,
        'itemTotal': orderItem.get_total,
        'productId': productId,
    }

    return JsonResponse(response_data, safe=False)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    print(context)

    return render(request, 'store/checkout.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.completed = True
    order.save()

    return JsonResponse("Payment completed..", safe=False)


#Samin Rahman
from .models import Event, Contributor
def index(request):
    event = Event.objects.all()
    return render(request, 'socialize/index.html', {
        #'show_socialize': False,
        # 'show_socialize': True,
        'socialize': event
    })
#   return HttpResponse('Hello django!')

def socializes_details(request, socializes_slug):
    user = request.user
    try:
        selected_Event = Event.objects.get(slug=socializes_slug)
        contributor,_ = Contributor.objects.get_or_create(user=request.user)
        selected_Event.contributor.add(contributor)

        return render(request, 'socialize/socializes-details.html', {
            'socialize_found': True,
            'socialize': selected_Event,
            'user': user,
        })

    except Exception as exc:
        print(exc)
        return render(request, 'socialize/socializes-details.html', {
            'socialize_found': False
        })

def registration_complete(request, socializes_slug):
    event_instance = Event.objects.get(slug=socializes_slug)
    return render(request, 'socialize/registration-complete.html', {
        'supervisor_email': event_instance.supervisor_email
    })


@csrf_exempt
def payment(request):
    
    try:
        
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        settings = { 'store_id': 'ripbo655c34b0d16ed', 'store_pass': 'ripbo655c34b0d16ed@ssl', 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = order.get_cart_total
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "1"
        post_body['success_url'] = "http://127.0.0.1:8000/shop/confirmed_pay/"
        post_body['fail_url'] = "http://127.0.0.1:8000/shop/checkout/"
        post_body['cancel_url'] = "http://127.0.0.1:8000/shop/checkout/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = 'jilan'
        post_body['cus_email'] = 'abc@gmail.com'
        post_body['cus_phone'] = '0123'
        
        post_body['cus_add1'] = 'Dhaka'
        post_body['cus_city'] = 'anywhere'
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = '15'
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"

        response = sslcz.createSession(post_body) 
        
        print(response)

        if(response['status'] == "SUCCESS"):
            return redirect(response['GatewayPageURL'])
        
        return redirect(response['GatewayPageURL'])
    except:
        return render(request, 'store/checkout.html')

@csrf_exempt
def payment_confirmed(request):
    # transaction_id = datetime.datetime.now().timestamp()
    

    
    # customer = request.user.customer
    # order, created = Order.objects.get_or_create(customer=customer, completed=False)

    
    # order.transaction_id = transaction_id
    
    # order.completed = True
    # order.save()

    # orderItem, created = OrderItem.objects.get_or_create(order=order)
    # orderItem.delete()

    return render( request, 'store/payment_successful.html')

def recipt(request):
    user = request.user
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'user':user, 'items': items, 'order': order, 'cartItems': cartItems}

    return render(request,'store/recipt.html',context)
