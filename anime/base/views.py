from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login,logout

from .models import  User
from .forms import MyUserCreationForm

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