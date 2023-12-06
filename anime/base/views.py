from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import  *
from .forms import MyUserCreationForm, UserForm
from django.http import JsonResponse
import json
from .utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Episode, Comment
from .utils import cartData
from django.views.decorators.csrf import csrf_exempt
import datetime
from sslcommerz_lib import SSLCOMMERZ 
from django.db.models import Avg
from django.views.generic import ListView


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
            return HttpResponse("Sorry you are not a registered user")
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
    all_animes = Anime.objects.all()
    
    search_query = request.GET.get('q', '')
    
    if search_query:
        all_animes = all_animes.filter(Q(name__icontains=search_query)).distinct()

    paginator = Paginator(all_animes, 6)
    page = request.GET.get('page', 1)

    try:
        all_animes = paginator.page(page)
    except PageNotAnInteger:
        all_animes = paginator.page(1)
    except EmptyPage:
        all_animes = paginator.page(paginator.num_pages)
        
    context = {
        'user': user,
        'all_animes': all_animes,
    }

    return render(request, 'base/home.html', context)


def userProfile(request,pk):

    user=User.objects.get(id=pk)
    

    context={'user':user,}
    return render(request,'base/profile.html',context)


def notification(request, pk):
    user = request.user
    
    contributor = Contributor.objects.filter(user=request.user)
    
    context = {'user': user, 'events': contributor}
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

        'socialize': event
    })


def socializes_details(request, socializes_slug):
    user = request.user
    try:
        selected_Event = Event.objects.get(slug=socializes_slug)
        

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
    selected_Event = Event.objects.get(slug=socializes_slug)
    contributor = Contributor.objects.create(user=request.user, event=selected_Event)
    

    event_instance = Event.objects.get(slug=socializes_slug)
    return render(request, 'socialize/registration-complete.html', {
        'supervisor_email': event_instance.supervisor_email
    })


@csrf_exempt
def payment(request):
    try:
        transaction_id = datetime.datetime.now().timestamp()
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        settings = { 'store_id': 'ripbo655c34b0d16ed', 'store_pass': 'ripbo655c34b0d16ed@ssl', 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = order.get_cart_total
        post_body['currency'] = "BDT"
        post_body['tran_id'] = transaction_id
        post_body['success_url'] = f"http://127.0.0.1:8000/shop/confirmed_pay/{customer.id}"
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
def payment_confirmed(request, pk):
    if request.method == 'post' or request.method =='POST':
        payment_data = request.POST
        customer = Customer.objects.get(id=pk)
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        
        if payment_data['status']=='VALID':

            trn=payment_data['tran_id']
            val_id = payment_data['val_id']
            
            request.session['payment_values_trn'] = trn
            request.session['payment_values_val_id'] = val_id
            
            order.transaction_id = trn
            order.completed = True
            order.save()
            orderid= order.id

            return render( request, 'store/payment_successful.html',{'trn':trn, 'valid':val_id, 'orderid':orderid})
    return render(request, 'store/checkout.html')

def order_history(request):
    user = request.user
    orders = Order.objects.filter(customer__user=user, completed=True).order_by('-date_ordered')
    context = {
        'user': user,
        'orders': orders
        
    }
    return render(request, 'store/orders.html', context)

def recipt(request, pk):
    order = Order.objects.get(id=pk)
    user = order.customer.user
    
    items = OrderItem.objects.filter(order=order)
    
    trn = request.session.get('payment_values_trn', None)
    val_id = request.session.get('payment_values_val_id', None)

    context = {
        'user': user,
        'items': items,
        'order': order,
        'trn': trn,
        'val_id': val_id,
    }

    return render(request,'store/recipt.html',context)


#Streaming Views
def anime_list(request):
    animes = Anime.objects.all()
    return render(request, 'anime_list.html', {'animes': animes})

@login_required(login_url='login')
def anime_detail(request, pk):
    anime = Anime.objects.get(id=pk)
    
    Anime.objects.filter(pk=anime.id).update(views=F('views') + 1)
    genres = anime.genres.all()
    episodes = Episode.objects.filter(anime=anime).order_by('number', 'name')
    anime_rating = AnimeRating.objects.filter(anime=anime).aggregate(Avg('rating'))
    try:
        raters= AnimeRating.objects.filter(user=request.user)
    except:
        raters= None

    if raters != None:
        print('found rating of current user')
    context = {
        'anime': anime,
        'genres': genres,
        'episodes': episodes,
        'rating': anime_rating,
    }

    if request.method=="POST":
        # if request.user.id in 
        comment= AnimeRating.objects.create(
            user=request.user,
            anime= anime,
            rating=request.POST.get('rating'),

        )
        
        return redirect('anime-detail', pk=anime.id)
    else:
        return render(request, 'streaming/anime_detail.html', context)

@login_required(login_url='login')
def episode_detail(request, pk):
    
    episode = Episode.objects.get(id=pk)
    comments = Comment.objects.filter(episode=episode)

    context = {
        'episode': episode,
        'comments': comments, 
    }

    if request.method=="POST":
        comment= Comment.objects.create(
            user=request.user,
            episode=episode,
            text=request.POST.get('body'),
        )
        
        return redirect('episode-detail', pk=episode.id)

    return render(request, 'streaming/episode_detail.html', context)

@login_required(login_url='login')
def delete_comment(request, pk):
    comment=Comment.objects.get(id=pk)
    episode = Episode.objects.get(id=comment.episode.id)

    if request.user != comment.user:
        return HttpResponse("You are not allowed here!!")
            
    if request.method=='POST':
        comment.delete()
        return redirect('episode-detail', pk=episode.id)
    
    return render(request, 'streaming/delete_comment.html')   

def genre_list(request):
    genres = Genre.objects.all()

    for genre in genres:
        genre.animes = Anime.objects.filter(genres=genre)

    return render(request, 'base/genre.html', {'genres': genres})

def favorite_anime(request):
    user = request.user
    favorite_animes = user.favorite_animes.all()
    
    anime_data = [
        {'id': anime.id, 'name': anime.name, 'is_favorite': anime in favorite_animes}
        for anime in Anime.objects.all()
    ]
    
    return render(request, 'base/favorites.html', {'favorite_animes': favorite_animes})

def remove_from_favorites(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    request.user.favorite_animes.remove(anime)
    return redirect('favorites')



def toggle_favorite(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    user = request.user

    if anime in user.favorite_animes.all():
        user.favorite_animes.remove(anime)
        is_favorite = False
    else:
        user.favorite_animes.add(anime)
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})
