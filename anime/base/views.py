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
from django.views.decorators.csrf import csrf_exempt
import datetime



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

def shop(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order=data['order']
    items=data['items']

    products = Product.objects.all()
    context={'products': products, 'cartItems': cartItems}

    return render(request,'store/shop.html',context)

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

    # Corrected method names
    cart_total = order.get_cart_items
    cart_totalPrice = order.get_cart_total

    return JsonResponse('item was added', safe=False)


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
from .forms import RegistrationForm
def index(request):
    event = Event.objects.all()
    return render(request, 'socialize/index.html', {
        #'show_socialize': False,
        # 'show_socialize': True,
        'socialize': event
    })
#   return HttpResponse('Hello django!')

def socializes_details(request, socializes_slug):
    # print(socializes_slug)
    try:
      selected_Event = Event.objects.get(slug=socializes_slug)
      if request.method == 'GET':
        # selected_socialize = Socialize.objects.get(slug=socializes_slug)
        registration_form = RegistrationForm()
        # return render(request, 'socialize/socializes-details.html', {
        # 'socialize_found': True,
        # 'socialize': selected_socialize,
        # 'form': registration_form
        #  'form': registration_form
        # 'socialize_title': selected_socialize['title'],
        # Using dot notation in this method
        # 'socialize_title': selected_socialize.title,
        # 'socialize_description': selected_socialize['description']
        # 'socialize_description': selected_socialize.description
    #    })
      else:
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
         # contributor = registration_form.save()
           user_email = registration_form.cleaned_data['email_address']
           user_phone = registration_form.cleaned_data['phone_number']
           contributor,_ = Contributor.objects.get_or_create(email_address=user_email, phone_number=user_phone)
           selected_Event.contributor.add(contributor)
           return redirect('registration_complete', socializes_slug=socializes_slug)


      return render(request, 'socialize/socializes-details.html', {
            'socialize_found': True,
            'socialize': selected_Event,
            'form': registration_form
        })

    except Exception as exc:
        print(exc)
        return render(request, 'socialize/socializes-details.html', {
            'socialize_found': False
        })

def registration_complete(request, socializes_slug):
  Event = Event.objects.get(slug=socializes_slug)
  return render(request, 'socialize/registration-complete.html', {
        'supervisor_email': Event.supervisor_email
    })
